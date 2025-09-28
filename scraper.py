#!/usr/bin/env python3
"""
Game Dataset Scraper - A tool for creating video game image datasets
by downloading YouTube gameplay videos and scraping web galleries.
"""

import argparse
import os
import sys
import yt_dlp
import glob
import cv2
from tqdm import tqdm

# Define all possible output directories to check for processed videos
OUTPUT_DIRECTORIES = ['dataset', 'real_images']

def extract_frames_from_video(video_path, target_fps, output_dir):
    """Extract frames from a video at specified FPS and save to output directory.
    
    returns:
        list: Paths to extracted frame image files
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        # Handle Error - video couldn't be opened
        print(f"Error: Could not open video file {video_path}")
        return []
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #If original video is 30 fps and you want 1 fps extraction
    # you need to extract every 30th frame
    frame_interval = int(original_fps / target_fps)
    
    # Calculate expected number of frames to extract for progress bar
    expected_extracted_frames = total_frames // frame_interval
    
    print(f"  Video info: {total_frames} total frames at {original_fps:.1f} FPS")
    print(f"  Will extract ~{expected_extracted_frames} frames at {target_fps} FPS")

    #extract frames in loop with progress bar
    frame_count = 0
    extracted_frames = []
    
    # Create progress bar for frame extraction
    with tqdm(total=total_frames, desc="  Extracting frames", unit="frame") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break #End of video

            #Only save frame if it matches our interval
            if frame_count % frame_interval == 0:
                #Get clean video name for filename
                video_name = os.path.splitext(os.path.basename(video_path))[0]
                clean_name = "".join(c for c in video_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                clean_name = clean_name.replace(' ', '_')  # Fix: move this BEFORE creating filename

                #Include video name in frame filename
                filename = f"{clean_name}_frame_{frame_count:06d}.jpg"
                filepath = os.path.join(output_dir, filename)
                cv2.imwrite(filepath, frame)
                extracted_frames.append(filepath)

            frame_count += 1
            pbar.update(1)  # Update progress bar

    cap.release()
    return extracted_frames


def get_video_title_from_query(query, num_videos):
    """Get video titles from YouTube search query without downloading.
    
    Args:
        query (str): YouTube search query
        num_videos (int): Number of videos to search for
        
    Returns:
        list: List of video titles that would be downloaded
    """
    search_query = f"ytsearch{num_videos}:{query}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Don't download, just get metadata
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if 'entries' in info:
                return [entry.get('title', 'Unknown') for entry in info['entries']]
            return []
    except Exception as e:
        print(f"Error getting video titles: {e}")
        return []

def check_for_duplicate_videos(query, num_videos, download_dir):
    """Check if videos from the query already exist in download directory.
    
    Args:
        query (str): YouTube search query
        num_videos (int): Number of videos to search for
        download_dir (str): Directory to check for existing videos
        
    Returns:
        tuple: (has_duplicates: bool, existing_videos: list, new_titles: list)
    """
    # Get titles of videos that would be downloaded
    new_titles = get_video_title_from_query(query, num_videos)
    if not new_titles:
        return False, [], []
    
    # Get existing video files in download directory
    existing_files = glob.glob(os.path.join(download_dir, "*.mp4")) + \
                    glob.glob(os.path.join(download_dir, "*.webm")) + \
                    glob.glob(os.path.join(download_dir, "*.mkv"))
    
    # Extract titles from existing files (remove extension)
    existing_titles = [os.path.splitext(os.path.basename(f))[0] for f in existing_files]
    
    # Check for duplicates
    duplicates = []
    existing_videos = []
    
    for new_title in new_titles:
        for existing_title in existing_titles:
            # Check if titles match (case-insensitive)
            if new_title.lower() == existing_title.lower():
                duplicates.append(new_title)
                # Find the corresponding file path
                for existing_file in existing_files:
                    if existing_title in existing_file:
                        existing_videos.append(existing_file)
                        break
    
    has_duplicates = len(duplicates) > 0
    return has_duplicates, existing_videos, new_titles

def download_youtube_videos(query, num_videos, download_dir):
    """Download youtube videos based on search query
    What to do:
    setup - create download configuration
    search - find videos matching query
    download - Get the videos and save them
    return - Give back list of downloaded file paths

    Args:
     query (str): What to search for (e.g., "Max Payne 1 gameplay")
        num_videos (int): How many videos to download (e.g., 3)
        download_dir (str): Where to save videos (e.g., "downloads")
    
    Returns:
        List: Paths to downloaded video files
    """
    #Create search query with number limit
    search_query = f"ytsearch{num_videos}:{query}"

    # Progress hook for download progress
    def progress_hook(d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                print(f"\rDownloading: {percent:.1f}% - {d.get('filename', '').split('/')[-1]}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n✓ Downloaded: {d.get('filename', '').split('/')[-1]}")

    # Configure download options
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'), #Where to download
        'quiet': True, #Less verbose output
        'progress_hooks': [progress_hook],  # Add progress tracking
    }

    # Get files that exist BEFORE downloading
    files_before = set(glob.glob(os.path.join(download_dir, "*")))

    # Download the videos
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])
        
        # Get files that exist AFTER downloading
        files_after = set(glob.glob(os.path.join(download_dir, "*")))
        
        # Find new files (difference between after and before)
        downloaded_files = list(files_after - files_before)
        
        return downloaded_files
    
    except Exception as e:
        print(f"Error downloading videos: {e}")
        return []  # Return empty list if failed

def download_youtube_url(url, download_dir):
    """Download a specific YouTube video from URL
    
    Args:
        url (str): Direct YouTube video URL
        download_dir (str): Where to save the video
        
    Returns:
        List: Path to downloaded video file
    """
    # Progress hook for download progress
    def progress_hook(d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                print(f"\rDownloading: {percent:.1f}% - {d.get('filename', '').split('/')[-1]}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n✓ Downloaded: {d.get('filename', '').split('/')[-1]}")

    # Configure download options
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'progress_hooks': [progress_hook],
    }

    # Get files that exist BEFORE downloading
    files_before = set(glob.glob(os.path.join(download_dir, "*")))

    # Download the video
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Get files that exist AFTER downloading
        files_after = set(glob.glob(os.path.join(download_dir, "*")))
        
        # Find new files (difference between after and before)
        downloaded_files = list(files_after - files_before)
        
        return downloaded_files
    
    except Exception as e:
        print(f"Error downloading video from URL: {e}")
        return []

def check_url_duplicate(url, download_dir):
    """Check if a video from the URL already exists in download directory.
    
    Args:
        url (str): YouTube video URL
        download_dir (str): Directory to check for existing videos
        
    Returns:
        tuple: (is_duplicate: bool, existing_video_path: str or None)
    """
    # Get video title from URL without downloading
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,  # Get full metadata
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'Unknown')
        
        # Get existing video files
        existing_files = glob.glob(os.path.join(download_dir, "*.mp4")) + \
                        glob.glob(os.path.join(download_dir, "*.webm")) + \
                        glob.glob(os.path.join(download_dir, "*.mkv"))
        
        # Check if any existing file matches the title
        for existing_file in existing_files:
            existing_title = os.path.splitext(os.path.basename(existing_file))[0]
            if video_title.lower() == existing_title.lower():
                return True, existing_file
        
        return False, None
    
    except Exception as e:
        print(f"Error checking URL duplicate: {e}")
        return False, None
    
def is_video_processed(video_path):
    """Check if frames have already been extracted for a given video.
    
    Args:
        video_path (str): Path to the video file

    Returns:
        bool: True if frames already exist, False otherwise
    """

    #Get video filename without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Clean the video name for use in filenames (like removing spaces, special chars)

    clean_name = "".join(c for c in video_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_name = clean_name.replace(' ', '_')

    # Look for frame files that start with this video name
    for directory in OUTPUT_DIRECTORIES:
        output_dir = directory
        pattern = os.path.join(output_dir, f"{clean_name}_frame_*.jpg")
        existing_frames = glob.glob(pattern)
        if len(existing_frames) > 0:
            return True #Found frames in this directory, video is processed
    
    return False # No frames found in any directory, video is unprocessed

def get_unprocessed_videos(video_list):
    """Filter a list of videos to only those that haven't been processed yet.
    
    Args:
        video_list (list): List of video file paths

    Returns:
        list: Subset of video_list that are unprocessed
    """
    unprocessed = []
    for video in video_list:
        if not is_video_processed(video):
            unprocessed.append(video)
    return unprocessed

def main():
    """Main function - handles command line arguments and coordinates scraping operations"""
    
    # Create argument parser to handle command-line options
    parser = argparse.ArgumentParser(description="Game Dataset Scraper")
    
    # Core argument: scraping mode (required)
    parser.add_argument('--mode', choices=["youtube", "gallery"],
                        required=True, help="Scraping mode: youtube videos or web gallery")
    
    # Output directory (optional, defaults to 'dataset')
    parser.add_argument("--outdir", default="dataset",
                        help="Output directory for dataset")
    
    # YouTube-specific arguments
    parser.add_argument("--query", 
                        help="YouTube search query (e.g., 'Max Payne 1 gameplay')")
    
    parser.add_argument("--num-videos",
                         type=int,
                         default=3,
                         help="Number of videos to download")
    
    parser.add_argument("--fps", 
                         type=float,
                         default=1.0,
                         help="Frames per second to extract from videos")
    
    parser.add_argument("--youtube-url",
                         help="Direct YouTube video URL to download")
    
    # Gallery-specific arguments
    parser.add_argument("--url",
                         help="Gallery URL to scrape images from")
    
    parser.add_argument("--selector",
                        help="CSS selector for images in gallery (e.g., '.screenshot img')")
    
    # Parse all command-line arguments
    args = parser.parse_args()

    # Create necessary directories if they don't exist
    os.makedirs(args.outdir, exist_ok=True)    # For final dataset images
    os.makedirs("downloads", exist_ok=True)    # For downloaded videos

    print(f"Starting scraper in {args.mode} mode...")
    print(f"Output directory: {args.outdir}")

    # Handle YouTube mode
    if args.mode == "youtube":
        if not args.query and not args.youtube_url:
            print("Error: Either --query or --youtube-url is required for YouTube mode")
            sys.exit(1)
        
        if args.query and args.youtube_url:
            print("Error: Please use either --query OR --youtube-url, not both")
            sys.exit(1)
        
        if args.query:
            print(f"YouTube mode - Query: {args.query}")
        else:
            print(f"YouTube mode - URL: {args.youtube_url}")
        print(f"Target FPS: {args.fps}")
        
        # Handle direct YouTube URL
        if args.youtube_url:
            print("Checking for duplicate video from URL...")
            is_duplicate, existing_video = check_url_duplicate(args.youtube_url, "downloads")
            
            if is_duplicate:
                print(f"⚠️ Video with same name found! Skipping download of duplicate video")
                print(f"  - {os.path.basename(existing_video)}")
                
                # Check if duplicate video needs processing
                if not is_video_processed(existing_video):
                    print("Duplicate video needs frame extraction")
                    videos_to_process = [existing_video]
                else:
                    print("Duplicate video has already been processed")
                    videos_to_process = []
            else:
                print("No duplicate found, downloading video from URL...")
                videos_to_process = download_youtube_url(args.youtube_url, "downloads")
        
        # Handle search query
        else:
            # Check for duplicate videos first
            print("Checking for duplicate videos...")
            has_duplicates, duplicate_videos, new_titles = check_for_duplicate_videos(args.query, args.num_videos, "downloads")
            
            if has_duplicates:
                print(f"⚠️ Video with same name found! Skipping download of duplicate video(s):")
                for i, title in enumerate(new_titles):
                    print(f"  - {title}")
                
                # Check if duplicate videos need processing
                unprocessed_duplicates = get_unprocessed_videos(duplicate_videos)
                
                if unprocessed_duplicates:
                    print(f"Found {len(unprocessed_duplicates)} duplicate videos that need frame extraction")
                    videos_to_process = unprocessed_duplicates
                else:
                    print("All duplicate videos have already been processed")
                    videos_to_process = []
            else:
                # No duplicates found, check for other existing videos or download new ones
                existing_videos = glob.glob("downloads/*.mp4") + glob.glob("downloads/*.webm") + glob.glob("downloads/*.mkv")
                
                if existing_videos:
                    print(f"Found {len(existing_videos)} existing videos (different from query)")
                    
                    # Check which videos haven't been processed yet
                    unprocessed_videos = get_unprocessed_videos(existing_videos)
                    
                    if unprocessed_videos:
                        print(f"Found {len(unprocessed_videos)} unprocessed videos, processing those first...")
                        print("Then downloading new video...")
                        # Process existing unprocessed videos AND download new ones
                        new_videos = download_youtube_videos(args.query, args.num_videos, "downloads")
                        videos_to_process = unprocessed_videos + new_videos
                    else:
                        print("All existing videos have been processed, downloading new ones...")
                        videos_to_process = download_youtube_videos(args.query, args.num_videos, "downloads")
                else:
                    print("No existing videos found, downloading...")
                    videos_to_process = download_youtube_videos(args.query, args.num_videos, "downloads")
        
        # Extract frames from the videos we're processing
        if videos_to_process:
            print(f"\n🎬 Processing {len(videos_to_process)} videos")
            all_extracted_frames = []
            
            # Progress bar for overall video processing
            for i, video_file in enumerate(videos_to_process, 1):
                print(f"\n📹 [{i}/{len(videos_to_process)}] Processing: {os.path.basename(video_file)}")
                frames = extract_frames_from_video(video_file, args.fps, args.outdir)
                all_extracted_frames.extend(frames)
                print(f"  ✓ Extracted {len(frames)} frames from this video")
            
            print(f"\n🎉 Complete! Extracted {len(all_extracted_frames)} total frames")
        else:
            print("No videos to process")
    
    # Handle gallery mode
    elif args.mode == "gallery":
        if not args.url or not args.selector:
            print("Error: --url and --selector are required for gallery mode")
            sys.exit(1)
        print(f"Gallery mode - URL: {args.url}")
        print(f"CSS selector: {args.selector}")
        # TODO: Implement gallery scraping

    print("Setup complete! Ready for implementation.")

# Entry point - only run main() if script is executed directly
if __name__ == "__main__":
    main()



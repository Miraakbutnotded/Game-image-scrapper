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
    
def is_video_processed(video_path, output_dir):
    """Check if frames have already been extracted for a given video.
    
    Args:
        video_path (str): Path to the video file
        output_dir (str): Directory where frames are saved

    Returns:
        bool: True if frames already exist, False otherwise
    """

    #Get video filename without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Clean the video name for use in filenames (like removing spaces, special chars)

    clean_name = "".join(c for c in video_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_name = clean_name.replace(' ', '_')

    # Look for frame files that start with this video name
    pattern = os.path.join(output_dir, f"{clean_name}_frame_*.jpg")
    existing_frames = glob.glob(pattern)

    #If we find frames from this video, it is already processed
    return len(existing_frames) > 0

def get_unprocessed_videos(video_list, output_dir):
    """Filter a list of videos to only those that haven't been processed yet.
    
    Args:
        video_list (list): List of video file paths
        output_dir (str): Directory where frames are saved

    Returns:
        list: Subset of video_list that are unprocessed
    """
    unprocessed = []
    for video in video_list:
        if not is_video_processed(video, output_dir):
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
        if not args.query:
            print("Error: --query is required for YouTube mode")
            sys.exit(1)
        
        print(f"YouTube mode - Query: {args.query}")
        print(f"Target FPS: {args.fps}")
        
        # Check for existing videos
        existing_videos = glob.glob("downloads/*.mp4") + glob.glob("downloads/*.webm") + glob.glob("downloads/*.mkv")
        
        if existing_videos:
            print(f"Found {len(existing_videos)} existing videos")
            
            # Check which videos haven't been processed yet
            unprocessed_videos = get_unprocessed_videos(existing_videos, args.outdir)
            
            if unprocessed_videos:
                print(f"Found {len(unprocessed_videos)} unprocessed videos, using those")
                videos_to_process = unprocessed_videos
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



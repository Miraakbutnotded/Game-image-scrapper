#!/usr/bin/env python3
"""
YouTube Video Processor - Handles YouTube video downloading and frame extraction
"""

import os
import glob
import cv2
import yt_dlp
from tqdm import tqdm
from typing import List, Tuple, Optional


class YouTubeProcessor:
    """Handles YouTube video downloading and frame extraction"""
    
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
    
    def get_video_titles_from_query(self, query: str, num_videos: int) -> List[str]:
        """Get video titles from YouTube search query without downloading."""
        search_query = f"ytsearch{num_videos}:{query}"
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
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
    
    def check_for_duplicate_videos(self, query: str, num_videos: int) -> Tuple[bool, List[str], List[str]]:
        """Check if videos from the query already exist in download directory."""
        new_titles = self.get_video_titles_from_query(query, num_videos)
        if not new_titles:
            return False, [], []
        
        existing_files = self._get_existing_video_files()
        existing_titles = [os.path.splitext(os.path.basename(f))[0] for f in existing_files]
        
        duplicates = []
        existing_videos = []
        
        for new_title in new_titles:
            for existing_title in existing_titles:
                if new_title.lower() == existing_title.lower():
                    duplicates.append(new_title)
                    for existing_file in existing_files:
                        if existing_title in existing_file:
                            existing_videos.append(existing_file)
                            break
        
        return len(duplicates) > 0, existing_videos, new_titles
    
    def check_url_duplicate(self, url: str) -> Tuple[bool, Optional[str]]:
        """Check if a video from the URL already exists in download directory."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
            
            existing_files = self._get_existing_video_files()
            
            for existing_file in existing_files:
                existing_title = os.path.splitext(os.path.basename(existing_file))[0]
                if video_title.lower() == existing_title.lower():
                    return True, existing_file
            
            return False, None
        
        except Exception as e:
            print(f"Error checking URL duplicate: {e}")
            return False, None
    
    def download_videos_by_query(self, query: str, num_videos: int) -> List[str]:
        """Download YouTube videos based on search query."""
        search_query = f"ytsearch{num_videos}:{query}"
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'progress_hooks': [self._progress_hook],
        }
        
        files_before = set(glob.glob(os.path.join(self.download_dir, "*")))
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([search_query])
            
            files_after = set(glob.glob(os.path.join(self.download_dir, "*")))
            downloaded_files = list(files_after - files_before)
            return downloaded_files
        
        except Exception as e:
            print(f"Error downloading videos: {e}")
            return []
    
    def download_video_by_url(self, url: str) -> List[str]:
        """Download a specific YouTube video from URL."""
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'progress_hooks': [self._progress_hook],
        }
        
        files_before = set(glob.glob(os.path.join(self.download_dir, "*")))
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            files_after = set(glob.glob(os.path.join(self.download_dir, "*")))
            downloaded_files = list(files_after - files_before)
            return downloaded_files
        
        except Exception as e:
            print(f"Error downloading video from URL: {e}")
            return []
    
    def _get_existing_video_files(self) -> List[str]:
        """Get list of existing video files in download directory."""
        return (glob.glob(os.path.join(self.download_dir, "*.mp4")) +
                glob.glob(os.path.join(self.download_dir, "*.webm")) +
                glob.glob(os.path.join(self.download_dir, "*.mkv")))
    
    def _progress_hook(self, d):
        """Progress hook for download progress display."""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                filename = d.get('filename', '').split('/')[-1]
                print(f"\rDownloading: {percent:.1f}% - {filename}", end='', flush=True)
        elif d['status'] == 'finished':
            filename = d.get('filename', '').split('/')[-1]
            print(f"\n✓ Downloaded: {filename}")


class FrameExtractor:
    """Handles frame extraction from video files"""
    
    def __init__(self, output_directories: List[str] = None):
        if output_directories is None:
            output_directories = ['dataset', 'real_images']
        self.output_directories = output_directories
    
    def extract_frames(self, video_path: str, target_fps: float, output_dir: str) -> List[str]:
        """Extract frames from a video at specified FPS."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return []
        
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = int(original_fps / target_fps)
        expected_extracted_frames = total_frames // frame_interval
        
        print(f"  Video info: {total_frames} total frames at {original_fps:.1f} FPS")
        print(f"  Will extract ~{expected_extracted_frames} frames at {target_fps} FPS")
        
        os.makedirs(output_dir, exist_ok=True)
        
        frame_count = 0
        extracted_frames = []
        
        with tqdm(total=total_frames, desc="  Extracting frames", unit="frame") as pbar:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    video_name = os.path.splitext(os.path.basename(video_path))[0]
                    clean_name = self._clean_filename(video_name)
                    
                    filename = f"{clean_name}_frame_{frame_count:06d}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    cv2.imwrite(filepath, frame)
                    extracted_frames.append(filepath)
                
                frame_count += 1
                pbar.update(1)
        
        cap.release()
        return extracted_frames
    
    def is_video_processed(self, video_path: str) -> bool:
        """Check if frames have already been extracted for a given video."""
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        clean_name = self._clean_filename(video_name)
        
        for directory in self.output_directories:
            pattern = os.path.join(directory, f"{clean_name}_frame_*.jpg")
            existing_frames = glob.glob(pattern)
            if len(existing_frames) > 0:
                return True
        
        return False
    
    def get_unprocessed_videos(self, video_list: List[str]) -> List[str]:
        """Filter a list of videos to only those that haven't been processed yet."""
        return [video for video in video_list if not self.is_video_processed(video)]
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename for use in file paths."""
        clean = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
        return clean.replace(' ', '_')
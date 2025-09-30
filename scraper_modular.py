#!/usr/bin/env python3
"""
Game Dataset Scraper - Refactored Main Application
A modular tool for creating video game image datasets
"""

import argparse
import sys
import os
from typing import List

from youtube_processor import YouTubeProcessor, FrameExtractor
from web_scraper import WebGalleryScraper
from dataset_manager import DatasetManager


class GameDatasetScraper:
    """Main application class coordinating all scraping operations"""
    
    def __init__(self):
        self.youtube_processor = YouTubeProcessor()
        self.frame_extractor = FrameExtractor()
        self.web_scraper = None  # Initialize when needed with specific output dir
        self.dataset_manager = DatasetManager()
    
    def run_youtube_mode(self, args) -> None:
        """Handle YouTube video downloading and frame extraction."""
        print(f"🎬 YouTube Mode")
        
        if args.query:
            print(f"   Search Query: {args.query}")
        else:
            print(f"   Video URL: {args.youtube_url}")
        
        print(f"   Target FPS: {args.fps}")
        print(f"   Output Directory: {args.outdir}")
        
        videos_to_process = []
        
        # Handle direct YouTube URL
        if args.youtube_url:
            print("\n🔍 Checking for duplicate video from URL...")
            is_duplicate, existing_video = self.youtube_processor.check_url_duplicate(args.youtube_url)
            
            if is_duplicate:
                print(f"⚠️  Video already exists: {os.path.basename(existing_video)}")
                if not self.frame_extractor.is_video_processed(existing_video):
                    print("   Video needs frame extraction")
                    videos_to_process = [existing_video]
                else:
                    print("   Video already processed")
                    videos_to_process = []
            else:
                print("   No duplicate found, downloading video...")
                videos_to_process = self.youtube_processor.download_video_by_url(args.youtube_url)
        
        # Handle search query
        else:
            print("\n🔍 Checking for duplicate videos...")
            has_duplicates, duplicate_videos, new_titles = self.youtube_processor.check_for_duplicate_videos(
                args.query, args.num_videos
            )
            
            if has_duplicates:
                print(f"⚠️  Found duplicate videos:")
                for title in new_titles:
                    print(f"   - {title}")
                
                unprocessed_duplicates = self.frame_extractor.get_unprocessed_videos(duplicate_videos)
                
                if unprocessed_duplicates:
                    print(f"   {len(unprocessed_duplicates)} duplicates need frame extraction")
                    videos_to_process = unprocessed_duplicates
                else:
                    print("   All duplicates already processed")
                    videos_to_process = []
            else:
                # Check for other existing videos
                existing_videos = self.youtube_processor._get_existing_video_files()
                
                if existing_videos:
                    print(f"📹 Found {len(existing_videos)} existing videos")
                    unprocessed_videos = self.frame_extractor.get_unprocessed_videos(existing_videos)
                    
                    if unprocessed_videos:
                        print(f"   Processing {len(unprocessed_videos)} unprocessed videos first...")
                        new_videos = self.youtube_processor.download_videos_by_query(
                            args.query, args.num_videos
                        )
                        videos_to_process = unprocessed_videos + new_videos
                    else:
                        print("   All existing videos processed, downloading new ones...")
                        videos_to_process = self.youtube_processor.download_videos_by_query(
                            args.query, args.num_videos
                        )
                else:
                    print("   No existing videos found, downloading...")
                    videos_to_process = self.youtube_processor.download_videos_by_query(
                        args.query, args.num_videos
                    )
        
        # Extract frames from videos
        if videos_to_process:
            print(f"\n🎬 Processing {len(videos_to_process)} videos")
            all_extracted_frames = []
            
            for i, video_file in enumerate(videos_to_process, 1):
                print(f"\n📹 [{i}/{len(videos_to_process)}] Processing: {os.path.basename(video_file)}")
                frames = self.frame_extractor.extract_frames(video_file, args.fps, args.outdir)
                all_extracted_frames.extend(frames)
                print(f"   ✓ Extracted {len(frames)} frames")
                
                # Create metadata for extracted frames
                if frames:
                    metadata_entries = []
                    source_info = {
                        'video_path': video_file,
                        'fps': args.fps,
                        'extraction_method': 'frame_interval'
                    }
                    
                    for frame_path in frames:
                        entry = self.dataset_manager.create_metadata_entry(
                            frame_path, 'youtube_frame', source_info
                        )
                        metadata_entries.append(entry)
                    
                    self.dataset_manager.save_metadata(metadata_entries)
            
            print(f"\n🎉 Complete! Extracted {len(all_extracted_frames)} total frames")
        else:
            print("ℹ️  No videos to process")
    
    def run_gallery_mode(self, args) -> None:
        """Handle web gallery scraping."""
        print(f"🕷️  Gallery Mode")
        print(f"   URL: {args.url}")
        print(f"   CSS Selector: {args.selector}")
        print(f"   Max Images: {args.num_images}")
        print(f"   Output Directory: {args.web_outdir}")
        
        # Initialize web scraper with specified output directory
        self.web_scraper = WebGalleryScraper(args.web_outdir)
        
        # Scrape images
        downloaded_files = self.web_scraper.scrape_gallery(
            args.url, args.selector, args.num_images
        )
        
        # Create metadata for downloaded images
        if downloaded_files:
            print(f"\n📊 Creating metadata for {len(downloaded_files)} images...")
            metadata_entries = []
            source_info = {
                'source_url': args.url,
                'css_selector': args.selector,
                'scraping_method': 'gallery'
            }
            
            for file_path in downloaded_files:
                if os.path.exists(file_path):
                    entry = self.dataset_manager.create_metadata_entry(
                        file_path, 'web_gallery', source_info
                    )
                    metadata_entries.append(entry)
            
            self.dataset_manager.save_metadata(metadata_entries)
            print(f"✅ Metadata saved for {len(metadata_entries)} files")
        
        print(f"\n🎉 Gallery scraping complete!")
    
    def run_google_images_mode(self, args) -> None:
        """Handle Google Images scraping specifically."""
        print(f"🔍 Google Images Mode")
        print(f"   Search URL: {args.url}")
        print(f"   Max Images: {args.num_images}")
        print(f"   Output Directory: {args.web_outdir}")
        
        # Initialize web scraper with specified output directory
        self.web_scraper = WebGalleryScraper(args.web_outdir)
        
        # Scrape Google Images
        downloaded_files = self.web_scraper.scrape_google_images(args.url, args.num_images)
        
        # Create metadata for downloaded images
        if downloaded_files:
            print(f"\n📊 Creating metadata for {len(downloaded_files)} images...")
            metadata_entries = []
            source_info = {
                'search_url': args.url,
                'scraping_method': 'google_images_enhanced'
            }
            
            for file_path in downloaded_files:
                if os.path.exists(file_path):
                    entry = self.dataset_manager.create_metadata_entry(
                        file_path, 'google_images', source_info
                    )
                    metadata_entries.append(entry)
            
            self.dataset_manager.save_metadata(metadata_entries)
            print(f"✅ Metadata saved for {len(metadata_entries)} files")
        
        print(f"\n🎉 Google Images scraping complete!")
    
    def show_summary(self) -> None:
        """Display dataset summary."""
        self.dataset_manager.print_summary()


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Game Dataset Scraper - Create video game image datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # YouTube video processing
  python scraper.py --mode youtube --query "Silent Hill 2 gameplay" --num-videos 3 --fps 1
  
  # Google Images scraping
  python scraper.py --mode gallery --url "https://www.google.com/search?q=foggy+town&udm=2" --selector img --num-images 100
  
  # General gallery scraping
  python scraper.py --mode gallery --url "https://example.com/gallery" --selector ".image img" --num-images 50
  
  # Show dataset summary
  python scraper.py --mode summary
        """
    )
    
    # Core arguments
    parser.add_argument('--mode', 
                       choices=['youtube', 'gallery', 'google-images', 'summary'],
                       required=True,
                       help='Scraping mode')
    
    # Output directories
    parser.add_argument('--outdir', 
                       default='dataset',
                       help='Output directory for video frames (default: dataset)')
    
    parser.add_argument('--video-outdir',
                       help='Custom output directory for video frames (overrides --outdir)')
    
    parser.add_argument('--web-outdir',
                       default='web_images',
                       help='Output directory for web images (default: web_images)')
    
    # YouTube mode arguments
    parser.add_argument('--query',
                       help='YouTube search query')
    
    parser.add_argument('--youtube-url',
                       help='Direct YouTube video URL')
    
    parser.add_argument('--num-videos',
                       type=int,
                       default=3,
                       help='Number of videos to download (default: 3)')
    
    parser.add_argument('--fps',
                       type=float,
                       default=1.0,
                       help='Frames per second to extract (default: 1.0)')
    
    # Gallery mode arguments  
    parser.add_argument('--url',
                       help='Gallery URL to scrape')
    
    parser.add_argument('--selector',
                       default='img',
                       help='CSS selector for images (default: img)')
    
    parser.add_argument('--num-images',
                       type=int,
                       default=50,
                       help='Maximum number of images to download (default: 50)')
    
    return parser


def main():
    """Main entry point."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Handle video output directory override
    if args.video_outdir:
        args.outdir = args.video_outdir
    
    print("🎮 Game Dataset Scraper - Modular Edition")
    print("=" * 50)
    
    scraper = GameDatasetScraper()
    
    if args.mode == 'youtube':
        if not args.query and not args.youtube_url:
            print("❌ Error: Either --query or --youtube-url is required for YouTube mode")
            sys.exit(1)
        
        if args.query and args.youtube_url:
            print("❌ Error: Use either --query OR --youtube-url, not both")
            sys.exit(1)
        
        scraper.run_youtube_mode(args)
    
    elif args.mode == 'gallery':
        if not args.url:
            print("❌ Error: --url is required for gallery mode")
            sys.exit(1)
        
        # Check if this is Google Images
        if 'google.com' in args.url and ('tbm=isch' in args.url or 'udm=2' in args.url):
            scraper.run_google_images_mode(args)
        else:
            scraper.run_gallery_mode(args)
    
    elif args.mode == 'google-images':
        if not args.url:
            print("❌ Error: --url is required for Google Images mode")
            sys.exit(1)
        scraper.run_google_images_mode(args)
    
    elif args.mode == 'summary':
        scraper.show_summary()
    
    print("\n✨ Operation complete!")


if __name__ == "__main__":
    main()
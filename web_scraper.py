#!/usr/bin/env python3
"""
Web Gallery Scraper - Handles web scraping from various image galleries
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from typing import List, Set, Optional


class WebGalleryScraper:
    """Handles web scraping from image galleries and Google Images"""
    
    def __init__(self, output_dir: str = "web_images"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # HTTP session for better performance
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_gallery(self, url: str, selector: str, max_images: int = 50) -> List[str]:
        """Generic gallery scraping using CSS selectors."""
        print(f"🕷️ Scraping gallery: {url}")
        print(f"Using CSS selector: {selector}")
        
        # Check if this is Google Images and use specialized scraping
        if self._is_google_images(url):
            return self.scrape_google_images(url, max_images)
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        img_elements = soup.select(selector)
        
        if not img_elements:
            print(f"⚠️ No images found with selector '{selector}'")
            return []
        
        print(f"Found {len(img_elements)} image elements")
        
        downloaded_files = []
        successful_downloads = 0
        
        with tqdm(total=min(len(img_elements), max_images), desc="Downloading images", unit="img") as pbar:
            for i, img in enumerate(img_elements[:max_images]):
                img_url = self._extract_image_url(img, url)
                if img_url:
                    filename = self._download_image(img_url, f"gallery_image_{i:04d}")
                    if filename:
                        downloaded_files.append(filename)
                        successful_downloads += 1
                
                pbar.update(1)
                time.sleep(0.1)  # Be respectful to servers
        
        print(f"✅ Successfully downloaded {successful_downloads} images")
        return downloaded_files
    
    def scrape_google_images(self, search_url: str, max_images: int = 100) -> List[str]:
        """Enhanced Google Images scraping with JavaScript parsing."""
        print(f"🔍 Enhanced Google Images scraping from: {search_url}")
        
        try:
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching Google Images: {e}")
            return []
        
        # Extract search term for filenames
        search_term = self._extract_search_term(search_url)
        
        # Multiple extraction methods for comprehensive image discovery
        image_urls = set()
        content = response.text
        
        # Method 1: Standard img src extraction
        soup = BeautifulSoup(content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and self._is_valid_image_url(src):
                image_urls.add(src)
        
        # Method 2-5: Regex patterns for JavaScript content
        patterns = [
            r'"(https://[^"]*\.(?:jpg|jpeg|png|gif|webp)[^"]*)"',
            r"'(https://[^']*\.(?:jpg|jpeg|png|gif|webp)[^']*)'",
            r'\["(https://[^"]*\.(?:jpg|jpeg|png|gif|webp)[^"]*)"\]',
            r'url\("?(https://[^")]*\.(?:jpg|jpeg|png|gif|webp)[^"]*)"?\)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if self._is_valid_image_url(match):
                    image_urls.add(match)
        
        image_urls = list(image_urls)[:max_images]
        
        print(f"🎯 Found {len(image_urls)} image URLs")
        
        if not image_urls:
            print("⚠️ No valid image URLs found")
            return []
        
        # Download images
        downloaded_files = []
        successful_downloads = 0
        failed_downloads = 0
        
        with tqdm(total=len(image_urls), desc="Downloading images", unit="img") as pbar:
            for i, img_url in enumerate(image_urls):
                filename = self._download_image(img_url, f"{search_term}_{i:04d}")
                if filename:
                    downloaded_files.append(filename)
                    successful_downloads += 1
                else:
                    failed_downloads += 1
                
                pbar.update(1)
                pbar.set_postfix({
                    'Success': successful_downloads,
                    'Failed': failed_downloads
                })
                
                time.sleep(0.1)  # Be respectful
        
        print(f"✅ Download complete!")
        print(f"   📥 Successfully downloaded: {successful_downloads}")
        print(f"   ❌ Failed downloads: {failed_downloads}")
        print(f"   📁 Files saved to: {self.output_dir}")
        
        return downloaded_files
    
    def _is_google_images(self, url: str) -> bool:
        """Check if URL is a Google Images search."""
        return 'google.com' in url and ('tbm=isch' in url or 'udm=2' in url)
    
    def _extract_search_term(self, url: str) -> str:
        """Extract search term from Google Images URL for filename."""
        patterns = [
            r'[?&]q=([^&]+)',
            r'/search\?.*?q=([^&]+)',
            r'search\?([^&]*?)(?:&|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                term = match.group(1).replace('+', '_').replace('%20', '_')
                return re.sub(r'[^\w\-_]', '', term)[:20]  # Limit length
        
        return "google_images"
    
    def _extract_image_url(self, img_element, base_url: str) -> Optional[str]:
        """Extract image URL from img element."""
        # Try different attributes
        for attr in ['src', 'data-src', 'data-original', 'data-lazy']:
            url = img_element.get(attr)
            if url:
                # Convert relative URLs to absolute
                if url.startswith('//'):
                    url = 'https:' + url
                elif url.startswith('/'):
                    url = urljoin(base_url, url)
                
                if self._is_valid_image_url(url):
                    return url
        
        return None
    
    def _is_valid_image_url(self, url: str) -> bool:
        """Check if URL appears to be a valid image."""
        if not url or len(url) < 10:
            return False
        
        # Skip obviously invalid URLs
        skip_patterns = [
            'data:', 'javascript:', 'blob:', 'about:',
            'logo', 'icon', 'sprite', 'placeholder',
            'avatar', 'profile', 'thumb', 'button'
        ]
        
        url_lower = url.lower()
        for pattern in skip_patterns:
            if pattern in url_lower:
                return False
        
        # Must be HTTP(S) and have image extension or be from image domains
        return (url.startswith(('http://', 'https://')) and 
                (re.search(r'\.(jpg|jpeg|png|gif|webp)', url_lower) or
                 any(domain in url_lower for domain in ['googleusercontent.com', 'imgur.com'])))
    
    def _download_image(self, url: str, base_filename: str) -> Optional[str]:
        """Download a single image from URL."""
        try:
            response = self.session.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '').lower()
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            else:
                # Try to get extension from URL
                parsed = urlparse(url)
                path = parsed.path.lower()
                if path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    ext = os.path.splitext(path)[1]
                else:
                    ext = '.jpg'  # Default
            
            filename = f"{base_filename}{ext}"
            filepath = os.path.join(self.output_dir, filename)
            
            # Handle duplicate filenames
            counter = 1
            while os.path.exists(filepath):
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{counter}{ext}"
                filepath = os.path.join(self.output_dir, filename)
                counter += 1
            
            # Download the image
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filepath
        
        except Exception as e:
            # Silently continue on individual failures
            return None
    
    def __del__(self):
        """Clean up session when object is destroyed."""
        if hasattr(self, 'session'):
            self.session.close()
# Game Dataset Scraper - TODO List

## ✅ Completed Features

### Core Infrastructure
- [x] Project setup with virtual environment
- [x] Requirements.txt with all dependencies
- [x] Command-line argument parsing (argparse)
- [x] Basic project structure and comprehensive README
- [x] Smart directory organization (video frames vs web images)

### YouTube Video Processing
- [x] YouTube video downloading with yt-dlp
- [x] Search query support (`ytsearch:N:query`)
- [x] Video download progress tracking
- [x] Smart file tracking (before/after download comparison)
- [x] Frame extraction from videos using OpenCV
- [x] Configurable FPS extraction rate
- [x] Frame extraction progress bars (tqdm)
- [x] Video name inclusion in frame filenames
- [x] Already-processed video detection
- [x] **Successfully extracted 954 Silent Hill game frames**

### Advanced Web Scraping (NEWLY COMPLETED)
- [x] **Enhanced Google Images scraping with JavaScript parsing**
- [x] **Multi-pattern URL extraction using 4+ regex patterns**
- [x] **Specialized `scrape_google_images()` function**
- [x] **Smart fallback mechanisms for maximum image discovery**
- [x] **Real-time progress tracking with success statistics**
- [x] **Robust error handling with graceful failure recovery**
- [x] **Automatic directory separation (web_images/ vs dataset/)**
- [x] **Successfully downloaded 99 atmospheric images (foggy town + Chernobyl)**
- [x] Skip reprocessing existing videos

### User Experience
- [x] Progress bars for downloads and frame extraction
- [x] Informative console output with emojis
- [x] Error handling for video processing
- [x] Multi-video processing support

## 🔄 TODO - Remaining Features

### Step 5: Gallery Scraping
- [x] **Web gallery image scraping**
  - [x] requests + BeautifulSoup integration
  - [x] CSS selector support for finding images
  - [x] Image download from gallery URLs
  - [x] Handle different image formats (jpg, png, webp, gif)
  - [x] Progress tracking for gallery scraping
  - [x] Error handling for network requests
  - [x] Configurable number of images to download
  - [x] Duplicate gallery check (existing images from same URL)
  - [x] User confirmation for continuing downloads
  - [x] Respectful scraping with delays

### Step 6: Metadata Management
- [ ] **CSV metadata creation**
  - [ ] Track image source (YouTube video vs gallery URL)
  - [ ] Record frame index for video frames
  - [ ] Store original video/gallery information
  - [ ] Add timestamp/date information
  - [ ] Create metadata.csv file
  - [ ] Append to existing metadata file

### Step 7: Duplicate Detection
- [ ] **Perceptual hashing for duplicate removal**
  - [ ] imagehash integration
  - [ ] Calculate perceptual hashes for all images
  - [ ] Compare hashes to find similar images
  - [ ] Remove or flag duplicate images
  - [ ] Configurable similarity threshold
  - [ ] Report on duplicates removed

## 🎯 Enhancements & Polish

### Error Handling & Robustness
- [ ] Better error messages for common issues
- [ ] Retry logic for failed downloads
- [ ] Validate input arguments more thoroughly
- [ ] Handle disk space issues
- [ ] Network connectivity checks

### Performance Improvements
- [ ] Parallel processing for multiple videos
- [ ] Optimize frame extraction for large videos
- [ ] Memory usage optimization
- [ ] Resume interrupted downloads

### Configuration & Usability
- [ ] Configuration file support (.config, .json)
- [ ] Dry-run mode (show what would be downloaded)
- [ ] Verbose/quiet output levels
- [ ] Statistics summary at end
- [ ] Log file creation

### Advanced Features
- [ ] Video quality selection options
- [ ] Custom frame selection (not just FPS-based)
- [ ] Image format conversion options
- [ ] Automatic image resizing
- [ ] Filter videos by duration/quality
- [ ] Batch processing from file list

## 🐛 Known Issues

- [ ] Frame extraction filename cleaning could be improved
- [ ] No validation of CSS selectors for gallery mode
- [ ] Large videos might consume significant memory
- [ ] No handling of age-restricted or private videos

## 📋 Testing Checklist

### YouTube Mode Testing
- [ ] Test with different game queries
- [ ] Test with various FPS settings (0.5, 1.0, 2.0)
- [ ] Test with multiple videos (1, 3, 5)
- [ ] Test resuming with existing videos
- [ ] Test error handling (invalid query, network issues)

### Gallery Mode Testing
- [ ] Test with MobyGames URLs
- [ ] Test with different CSS selectors
- [ ] Test with various image galleries
- [ ] Test error handling (invalid URL, no images)

### Integration Testing
- [ ] Test mixed workflows (YouTube + Gallery)
- [ ] Test metadata accuracy
- [ ] Test duplicate detection effectiveness
- [ ] Test with large datasets

## 🚀 Future Ideas

- [ ] GUI interface (tkinter or web-based)
- [ ] Docker containerization
- [ ] Cloud storage integration (AWS S3, Google Drive)
- [ ] Database support for metadata (SQLite)
- [ ] API for external integrations
- [ ] Machine learning integration for image classification
- [ ] Automatic game detection from images
- [ ] Video game screenshot quality scoring

---

## Quick Commands Reference

```bash
# Download and extract from YouTube
python3 scraper.py --mode youtube --query "Max Payne 1 gameplay" --num-videos 3 --fps 1.0

# Scrape from web gallery (when implemented)
python3 scraper.py --mode gallery --url "https://example.com/screenshots" --selector ".screenshot img"

# Check current status
ls downloads/  # Downloaded videos
ls dataset/    # Extracted images
```

## Development Notes

- Keep functions focused and single-purpose
- Add comprehensive error handling
- Document all new functions with docstrings
- Test each feature thoroughly before moving to next
- Consider breaking into multiple files if it gets too large

---
*Last updated: December 2024*
# Image Datase## 🚀 Quick Start

```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # Windows (use source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt

# 2. Extract frames from YouTube videos
python scraper.py --mode youtube --query "Silent Hill 2 gameplay" --num-videos 3 --fps 1

# 3. Scrape Google Images (enhanced method)
python scraper.py --mode gallery --url "https://www.google.com/search?q=foggy+town&udm=2" --selector img --num-images 100

# 4. Scrape gaming websites
python scraper.py --mode gallery --url "https://steamcommunity.com/app/12345/screenshots" --selector ".screenshot img" --num-images 50

# 5. View dataset summary
python scraper.py --mode summary
```

## 📋 More Examples

### YouTube Video Processing
```bash
# High-quality frame extraction
python scraper.py --mode youtube --query "Resident Evil 4 walkthrough" --num-videos 1 --fps 2

# Multiple videos with custom output directory
python scraper.py --mode youtube --query "horror games compilation" --num-videos 5 --fps 0.5 --outdir horror_frames

# Direct YouTube URL
python scraper.py --mode youtube --youtube-url "https://youtube.com/watch?v=VIDEO_ID" --fps 1
```

### Advanced Web Scraping
```bash
# Google Images with specific search terms
python scraper.py --mode gallery --url "https://www.google.com/search?q=abandoned+places&udm=2" --num-images 200

# Gaming websites
python scraper.py --mode gallery --url "https://www.mobygames.com/game/123/screenshots/" --selector ".screenshot img" --num-images 30

# Custom output directory for web images
python scraper.py --mode gallery --url "https://example.com/gallery" --selector "img" --web-outdir custom_images
```ade this because I couldn't find a image database to train my models. With this, you will be able to scrape youtube videos and extract frames from it etc. 

Basically you can gather your own dataset from multiple sources including YouTube gameplay videos, Google Images, and gaming websites.

## ✨ Features
- **YouTube Processing**: Download videos and extract frames at custom FPS
- **Google Images Scraping**: Advanced parsing with 80-90% success rates  
- **Gallery Scraping**: Extract images from gaming websites
- **Smart Organization**: Automatic file separation and metadata tracking
- **Progress Tracking**: Real-time download progress with success statistics
- **Error Recovery**: Continues downloading despite individual failures

## � Quick Start

```bash
# 1. Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Extract frames from YouTube videos
python scraper.py --mode youtube --query "Silent Hill 2 gameplay" --num-videos 3 --fps 1

# 3. Scrape Google Images (enhanced method)
python scraper.py --mode gallery --url "https://www.google.com/search?q=foggy+town&udm=2" --selector img --num-images 100

# 4. Scrape gaming websites
python scraper.py --mode gallery --url "https://steamcommunity.com/app/12345/screenshots" --selector ".screenshot img" --num-images 50
```

## 📁 Output Structure
```
game-dataset-scraper/
├── scraper.py              # Main scraper tool
├── downloads/              # Downloaded YouTube videos  
├── dataset/                # Extracted video frames
├── web_images/             # Downloaded web gallery images
└── metadata.json           # File tracking and metadata
```

## ⚙️ Command Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--mode` | youtube, gallery, summary | `--mode youtube` |
| `--query` | YouTube search terms | `--query "Silent Hill 2"` |
| `--youtube-url` | Direct YouTube video URL | `--youtube-url "https://youtube.com/watch?v=ID"` |
| `--fps` | Frame extraction rate | `--fps 1.0` |
| `--num-videos` | Number of videos to download | `--num-videos 3` |
| `--num-images` | Max images to download | `--num-images 100` |
| `--url` | Gallery URL to scrape | `--url "https://example.com/gallery"` |
| `--selector` | CSS selector for images | `--selector ".screenshot img"` |
| `--outdir` | Video frames directory | `--outdir dataset` |
| `--web-outdir` | Web images directory | `--web-outdir web_images` |


## 🔍 Tips & Best Practices

### For YouTube:
- Use specific game titles for better results: `"Silent Hill 2 walkthrough"` vs `"horror games"`
- Lower FPS (0.5-1.0) for cutscenes, higher FPS (2.0+) for gameplay
- Check `downloads/` folder to avoid re-downloading videos

### For Google Images:
- Use the new Google Images format with `udm=2` parameter
- Try different search terms: `"abandoned places fog"`, `"horror game screenshots"`
- Expect 80-90% success rate due to modern anti-scraping measures

### For Gaming Websites:
- Use browser developer tools to find the right CSS selector
- Steam community pages work well with `.screenshot img`
- MobyGames uses `.screenshot img` or similar selectors

---
**Perfect for creating datasets for CycleGAN, image classification, and game asset research** 🎮✨
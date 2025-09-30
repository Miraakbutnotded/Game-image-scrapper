# Game Dataset Scraper# Image Dataset Scraper



A powerful Python tool for building image datasets from YouTube videos and web galleries, specifically designed for game asset research, machine learning training data, and visual content analysis.I made this because I couldn't find a image database to train my models. With this, you will be able to scrape YouTube videos and extract frames from it etc. 



## FeaturesBasically you can gather your own dataset from multiple sources including YouTube gameplay videos, Google Images, and gaming websites.



### YouTube Video Processing## Features

- **Smart Frame Extraction**: Configurable FPS with intelligent frame selection- **YouTube Processing**: Download videos and extract frames at custom FPS

- **Batch Processing**: Download and process multiple videos automatically  - **Google Images Scraping**: Advanced parsing with 80-90% success rates  

- **Query-Based Search**: Find videos using search terms or direct URLs- **Gallery Scraping**: Extract images from gaming websites

- **Duplicate Prevention**: Skip already processed videos to save time- **Smart Organization**: Automatic file separation and metadata tracking

- **Progress Tracking**: Real-time download progress with success statistics

### Enhanced Web Scraping- **Error Recovery**: Continues downloading despite individual failures

- **Google Images Support**: Advanced scraping with 80-90% success rates

- **Multi-Pattern Detection**: Finds images through various URL patterns## Quick Start

- **Gaming Site Optimization**: Tested on Steam, MobyGames, and community sites

- **Error Recovery**: Continues downloading despite individual failures```bash

# 1. Setup

### Modular Architecturepython -m venv venv

- **youtube_processor.py**: Specialized YouTube downloading and frame extractionvenv\Scripts\activate  # Windows (use source venv/bin/activate on Linux/Mac)

- **web_scraper.py**: Enhanced web gallery and Google Images scrapingpip install -r requirements.txt

- **dataset_manager.py**: File organization, metadata tracking, and duplicate detection

- **scraper_modular.py**: Main orchestrator with comprehensive CLI# 2. Extract frames from YouTube videos

python scraper.py --mode youtube --query "Silent Hill 2 gameplay" --num-videos 3 --fps 1

## Quick Start

# 3. Scrape Google Images (enhanced method)

```bashpython scraper.py --mode gallery --url "https://www.google.com/search?q=foggy+town&udm=2" --selector img --num-images 100

# 1. Setup

python -m venv venv# 4. Scrape gaming websites

venv\Scripts\activate  # Windowspython scraper.py --mode gallery --url "https://steamcommunity.com/app/12345/screenshots" --selector ".screenshot img" --num-images 50

pip install -r requirements.txt

# 5. View dataset summary

# 2. Extract frames from YouTube videospython scraper.py --mode summary

python scraper_modular.py --mode youtube --query "Silent Hill 2 gameplay" --num-videos 3 --fps 1```



# 3. Scrape Google Images (enhanced method)## Project Structure

python scraper_modular.py --mode gallery --url "https://www.google.com/search?q=foggy+town&udm=2" --selector img --num-images 100```

game-dataset-scraper/

# 4. Scrape gaming websites├── scraper.py              # Main scraper tool

python scraper_modular.py --mode gallery --url "https://steamcommunity.com/app/12345/screenshots" --selector ".screenshot img" --num-images 50├── scraper_modular.py      # Enhanced modular version

```├── youtube_processor.py    # YouTube video handling

├── web_scraper.py          # Web scraping functionality

## Output Structure├── dataset_manager.py      # File organization & metadata

```├── downloads/              # Downloaded YouTube videos  

game-dataset-scraper/├── dataset/                # Extracted video frames

├── scraper_modular.py      # Main scraper tool (modular version)├── web_images/             # Downloaded web gallery images

├── scraper.py              # Legacy monolithic version└── metadata.json           # File tracking and metadata

├── youtube_processor.py    # YouTube functionality```

├── web_scraper.py          # Web scraping functionality  

├── dataset_manager.py      # Dataset organization## More Examples

├── downloads/              # Downloaded YouTube videos  

├── dataset/                # Extracted video frames### YouTube Video Processing

├── web_images/             # Downloaded web gallery images```bash

└── metadata.json           # File tracking and metadata# High-quality frame extraction

```python scraper.py --mode youtube --query "Resident Evil 4 walkthrough" --num-videos 1 --fps 2



## Command Reference# Multiple videos with custom output directory

python scraper.py --mode youtube --query "horror games compilation" --num-videos 5 --fps 0.5 --outdir horror_frames

| Option | Description | Example |

|--------|-------------|---------|# Direct YouTube URL

| `--mode` | youtube, gallery, summary | `--mode youtube` |python scraper.py --mode youtube --youtube-url "https://youtube.com/watch?v=VIDEO_ID" --fps 1

| `--query` | YouTube search terms | `--query "Silent Hill 2"` |```

| `--youtube-url` | Direct YouTube video URL | `--youtube-url "https://youtube.com/watch?v=ID"` |

| `--fps` | Frame extraction rate | `--fps 1.0` |### Advanced Web Scraping

| `--num-videos` | Number of videos to download | `--num-videos 3` |```bash

| `--num-images` | Max images to download | `--num-images 100` |# Google Images with specific search terms

| `--url` | Gallery URL to scrape | `--url "https://example.com/gallery"` |python scraper.py --mode gallery --url "https://www.google.com/search?q=abandoned+places&udm=2" --num-images 200

| `--selector` | CSS selector for images | `--selector ".screenshot img"` |

| `--outdir` | Video frames directory | `--outdir dataset` |# Gaming websites

| `--web-outdir` | Web images directory | `--web-outdir web_images` |python scraper.py --mode gallery --url "https://www.mobygames.com/game/123/screenshots/" --selector ".screenshot img" --num-images 30



## Installation# Custom output directory for web images

python scraper.py --mode gallery --url "https://example.com/gallery" --selector "img" --web-outdir custom_images

```bash```

git clone https://github.com/yourusername/game-dataset-scraper.git- **YouTube Processing**: Download videos and extract frames at custom FPS

cd game-dataset-scraper- **Google Images Scraping**: Advanced parsing with 80-90% success rates  

python -m venv venv- **Gallery Scraping**: Extract images from gaming websites

venv\Scripts\activate  # Windows- **Smart Organization**: Automatic file separation and metadata tracking

# or: source venv/bin/activate  # Linux/Mac- **Progress Tracking**: Real-time download progress with success statistics

pip install -r requirements.txt- **Error Recovery**: Continues downloading despite individual failures

```

## � Quick Start

## Usage Examples

```bash

### YouTube Frame Extraction# 1. Setup

```bashpython -m venv venv

# Extract frames from Silent Hill 2 cutscenes at 1 FPSvenv\Scripts\activate  # Windows

python scraper_modular.py --mode youtube --query "Silent Hill 2 ALL CUTSCENES" --fps 1 --num-videos 1pip install -r requirements.txt



# Process multiple horror game videos# 2. Extract frames from YouTube videos

python scraper_modular.py --mode youtube --query "horror game atmosphere" --fps 0.5 --num-videos 5python scraper.py --mode youtube --query "Silent Hill 2 gameplay" --num-videos 3 --fps 1

```

# 3. Scrape Google Images (enhanced method)

### Google Images Scrapingpython scraper.py --mode gallery --url "https://www.google.com/search?q=foggy+town&udm=2" --selector img --num-images 100

```bash

# Scrape atmospheric images# 4. Scrape gaming websites

python scraper_modular.py --mode gallery --url "https://www.google.com/search?q=abandoned+foggy+town&udm=2" --num-images 100python scraper.py --mode gallery --url "https://steamcommunity.com/app/12345/screenshots" --selector ".screenshot img" --num-images 50

```

# Download specific game screenshots

python scraper_modular.py --mode gallery --url "https://www.google.com/search?q=Silent+Hill+2+screenshots&udm=2" --num-images 50## 📁 Output Structure

``````

game-dataset-scraper/

### Gaming Website Scraping├── scraper.py              # Main scraper tool

```bash├── downloads/              # Downloaded YouTube videos  

# Steam community screenshots├── dataset/                # Extracted video frames

python scraper_modular.py --mode gallery --url "https://steamcommunity.com/app/105420/screenshots/" --selector ".screenshot img" --num-images 30├── web_images/             # Downloaded web gallery images

└── metadata.json           # File tracking and metadata

# MobyGames gallery```

python scraper_modular.py --mode gallery --url "https://www.mobygames.com/game/silent-hill-2/screenshots" --selector ".screenshot img" --num-images 25

```## ⚙️ Command Reference



## Tips & Best Practices| Option | Description | Example |

|--------|-------------|---------|

### For YouTube| `--mode` | youtube, gallery, summary | `--mode youtube` |

- Use specific game titles for better results: `"Silent Hill 2 walkthrough"` vs `"horror games"`| `--query` | YouTube search terms | `--query "Silent Hill 2"` |

- Lower FPS (0.5-1.0) for cutscenes, higher FPS (2.0+) for gameplay| `--youtube-url` | Direct YouTube video URL | `--youtube-url "https://youtube.com/watch?v=ID"` |

- Check `downloads/` folder to avoid re-downloading videos| `--fps` | Frame extraction rate | `--fps 1.0` |

| `--num-videos` | Number of videos to download | `--num-videos 3` |

### For Google Images| `--num-images` | Max images to download | `--num-images 100` |

- Use the new Google Images format with `udm=2` parameter| `--url` | Gallery URL to scrape | `--url "https://example.com/gallery"` |

- Try different search terms: `"abandoned places fog"`, `"horror game screenshots"`| `--selector` | CSS selector for images | `--selector ".screenshot img"` |

- Expect 80-90% success rate due to modern anti-scraping measures| `--outdir` | Video frames directory | `--outdir dataset` |

| `--web-outdir` | Web images directory | `--web-outdir web_images` |

### For Gaming Websites

- Use browser developer tools to find the right CSS selector

- Steam community pages work well with `.screenshot img`## 🔍 Tips & Best Practices

- MobyGames uses `.screenshot img` or similar selectors

### For YouTube:

## Requirements- Use specific game titles for better results: `"Silent Hill 2 walkthrough"` vs `"horror games"`

- Lower FPS (0.5-1.0) for cutscenes, higher FPS (2.0+) for gameplay

- Python 3.7+- Check `downloads/` folder to avoid re-downloading videos

- yt-dlp (for YouTube downloads)

- opencv-python (for frame extraction)### For Google Images:

- requests (for web scraping)- Use the new Google Images format with `udm=2` parameter

- beautifulsoup4 (for HTML parsing)- Try different search terms: `"abandoned places fog"`, `"horror game screenshots"`

- Expect 80-90% success rate due to modern anti-scraping measures

## Architecture

### For Gaming Websites:

The scraper is built with a modular architecture for maintainability and extensibility:- Use browser developer tools to find the right CSS selector

- Steam community pages work well with `.screenshot img`

- **YouTubeProcessor**: Handles video downloading and frame extraction- MobyGames uses `.screenshot img` or similar selectors

- **WebGalleryScraper**: Manages web scraping with multiple fallback methods

- **DatasetManager**: Organizes files, tracks metadata, and prevents duplicates---

- **GameDatasetScraper**: Main orchestrator coordinating all components**Perfect for creating datasets for CycleGAN, image classification, and game asset research** 🎮✨

Perfect for creating datasets for CycleGAN, image classification, and game asset research.
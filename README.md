# Game Dataset Scraper

A Python tool for creating video game image datasets by:
- Downloading YouTube gameplay videos
- Extracting frames from videos
- Scraping screenshots from web galleries
- Managing metadata and removing duplicates

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Download from YouTube:
```bash
python scraper.py --mode youtube --query "Max Payne 1 gameplay" --num-videos 5 --fps 1 --outdir dataset
```

Scrape from gallery:
```bash
python scraper.py --mode gallery --url "https://example.com/screenshots" --selector ".screenshot img" --outdir dataset
```

## Project Structure

```
game-dataset-scraper/
├── scraper.py          # Main script
├── requirements.txt    # Dependencies
├── downloads/          # Downloaded videos
├── dataset/           # Extracted images
└── metadata.csv       # Image metadata
```
"""Preprocessing module for news articles."""

import csv
import re
from pathlib import Path
from typing import List, Dict, Any, Set
from datetime import datetime
import sys

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

RAW_DATA_DIR = BASE_DIR / "dataM" / "raw" / "csv"
PROCESSED_DATA_DIR = BASE_DIR / "dataM" / "processed"

MIN_ARTICLE_LENGTH = 50
MAX_ARTICLE_LENGTH = 10000


def load_raw_news(file_path: Path) -> List[Dict[str, str]]:
    """Load raw news data from CSV file."""
    articles = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            articles.append(row)
    return articles


def clean_text_for_sentiment(text: str) -> str:
    """Clean text while preserving sentiment signals."""
    if not text or not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'http[s]?://\S+', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove HTML entities
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    # Preserve punctuation, normalize whitespace only
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_text_basic(text: str) -> str:
    """Clean text with minimal changes for validation only."""
    if not text or not isinstance(text, str):
        return ""
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_timestamp(timestamp_str: str) -> str:
    """Parse and normalize timestamp."""
    if not timestamp_str:
        return ""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.isoformat()
    except (ValueError, AttributeError):
        return ""


def combine_article_text(article: Dict[str, Any]) -> str:
    """Combine title, description, and content for validation purposes."""
    parts = []
    for field in ["title", "description", "content"]:
        text = article.get(field, "")
        if text:
            parts.append(clean_text_basic(text))
    return " ".join(parts)


def is_duplicate(article_url: str, existing_urls: Set[str]) -> bool:
    """Check if article URL already exists."""
    return article_url in existing_urls


def is_valid_article(article: Dict[str, Any], combined_text: str) -> bool:
    """Validate if article meets quality criteria."""
    if len(combined_text) < MIN_ARTICLE_LENGTH or len(combined_text) > MAX_ARTICLE_LENGTH:
        return False
    if not article.get("title") and not article.get("description"):
        return False
    return bool(article.get("url"))


def preprocess_articles(data: List[Dict[str, str]]) -> tuple[List[Dict[str, str]], Dict[str, int]]:
    """Preprocess articles by extracting and filtering."""
    processed = []
    seen_urls: Set[str] = set()
    
    metrics = {
        "total_articles": len(data),
        "duplicates_removed": 0,
        "too_short": 0,
        "too_long": 0,
        "invalid_format": 0,
        "valid_articles": 0,
        "missing_title": 0,
        "missing_description": 0,
        "missing_content": 0,
    }
    
    for article in data:
        try:
            url = article.get("url", "")
            if is_duplicate(url, seen_urls):
                metrics["duplicates_removed"] += 1
                continue
            
            combined_text = combine_article_text(article)
            
            if not is_valid_article(article, combined_text):
                text_length = len(combined_text)
                if text_length < MIN_ARTICLE_LENGTH:
                    metrics["too_short"] += 1
                elif text_length > MAX_ARTICLE_LENGTH:
                    metrics["too_long"] += 1
                else:
                    metrics["invalid_format"] += 1
                continue
            
            if not article.get("title"):
                metrics["missing_title"] += 1
            if not article.get("description"):
                metrics["missing_description"] += 1
            if not article.get("content"):
                metrics["missing_content"] += 1
            
            # Prepare sentiment-safe text for analysis
            text_for_analysis = clean_text_for_sentiment(combined_text)
            
            processed_article = {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "content": article.get("content", ""),
                "text_for_analysis": text_for_analysis,
                "url": article.get("url", ""),
                "published_at": parse_timestamp(article.get("published_at", "")),
                "source": article.get("source_name", ""),
                "author": article.get("author", ""),
                "image_url": article.get("url_to_image", ""),
            }
            
            processed.append(processed_article)
            seen_urls.add(url)
            metrics["valid_articles"] += 1
            
        except Exception as e:
            print(f"  ⚠ Error: {e}")
            metrics["invalid_format"] += 1
    
    return processed, metrics


def save_processed_news(file_path: Path, articles: List[Dict[str, str]]) -> int:
    """Save processed articles to CSV, appending to existing file if present.
    
    Returns: Number of new articles added.
    """
    if not articles:
        return 0
    
    fieldnames = ["title", "description", "content", "text_for_analysis", "url", "published_at", "source", "author", "image_url"]
    file_exists = file_path.exists()
    
    # If file exists, read existing URLs to avoid duplicates
    existing_urls = set()
    if file_exists:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("url"):
                        existing_urls.add(row["url"])
        except Exception as e:
            print(f"  Warning: Could not read existing file {file_path.name}: {e}")
    
    # Filter out duplicate URLs
    new_articles = [a for a in articles if a.get("url") not in existing_urls]
    
    if not new_articles:
        return 0
    
    # Append to file
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        for article in new_articles:
            writer.writerow({key: article.get(key, "") for key in fieldnames})
    
    return len(new_articles)


def save_quality_metrics(file_path: Path, metrics: Dict[str, int]) -> None:
    """Save quality metrics to CSV."""
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Count"])
        for key, value in metrics.items():
            writer.writerow([key, value])


def main():
    """Process all raw news files from timeframe subdirectories."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if not RAW_DATA_DIR.exists():
        print(f"Raw data directory not found: {RAW_DATA_DIR}")
        return
    
    # Search for news files in subdirectories (1/, 5/, 10/, etc.)
    raw_files = sorted(RAW_DATA_DIR.glob("*/news_*.csv"))
    
    if not raw_files:
        print(f"No news files found in {RAW_DATA_DIR}/*/ subdirectories")
        return
    
    print(f"\n📰 Processing {len(raw_files)} file(s)...\n")
    
    total_metrics = {
        "total_articles": 0,
        "duplicates_removed": 0,
        "too_short": 0,
        "too_long": 0,
        "invalid_format": 0,
        "valid_articles": 0,
        "missing_title": 0,
        "missing_description": 0,
        "missing_content": 0,
    }
    
    for raw_file in raw_files:
        timeframe = raw_file.parent.name
        timeframe_dir = PROCESSED_DATA_DIR / f"{timeframe}_days_processed"
        timeframe_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"  Processing {timeframe}/{raw_file.name}...")
        try:
            data = load_raw_news(raw_file)
            articles, metrics = preprocess_articles(data)
            
            output_file = timeframe_dir / f"processed_{raw_file.stem}.csv"
            new_count = save_processed_news(output_file, articles)
            
            for key in total_metrics:
                total_metrics[key] += metrics.get(key, 0)
            
            if new_count > 0:
                print(f"    ✓ Added {new_count} new articles to {timeframe_dir.name}/{output_file.name}")
            else:
                print(f"    ℹ No new articles (all {len(articles)} were duplicates)")
            print(f"      • Duplicates: {metrics['duplicates_removed']}, Too short: {metrics['too_short']}")
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total: {total_metrics['total_articles']} | Valid: {total_metrics['valid_articles']} | Duplicates: {total_metrics['duplicates_removed']}")
    print()


if __name__ == "__main__":
    main()

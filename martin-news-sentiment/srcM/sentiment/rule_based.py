"""Rule-based sentiment analysis for news articles."""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import sys

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

PROCESSED_DATA_DIR = BASE_DIR / "dataM" / "processed"
RESULTS_DIR = BASE_DIR / "resultsM"

# Simple rule-based lexicons
POSITIVE_WORDS = {
    "gain", "up", "surge", "rally", "bull", "rise", "advance", "strengthen",
    "growth", "profit", "success", "strong", "outperform", "beat", "exceed",
    "recovery", "upbeat", "positive", "bullish", "momentum", "opportunity"
}

NEGATIVE_WORDS = {
    "loss", "down", "drop", "fall", "bear", "decline", "weaken", "plunge",
    "crash", "break", "negative", "bearish", "miss", "fail", "weak",
    "slump", "downside", "risk", "concern", "threat", "problem"
}


def calculate_sentiment_score(text: str) -> float:
    """
    Calculate sentiment score based on positive/negative word occurrences.
    
    Args:
        text: Text to analyze (title, description, or content)
        
    Returns:
        Sentiment score between -1 (very negative) and 1 (very positive)
    """
    if not text:
        return 0.0
    
    text_lower = text.lower()
    words = set(text_lower.split())
    
    positive_count = len(words & POSITIVE_WORDS)
    negative_count = len(words & NEGATIVE_WORDS)
    total = positive_count + negative_count
    
    if total == 0:
        return 0.0
    
    return (positive_count - negative_count) / total


def analyze_article(article: Dict[str, str]) -> Dict[str, Any]:
    """
    Analyze sentiment of an article.
    
    Args:
        article: Preprocessed article dictionary
        
    Returns:
        Article with sentiment analysis results
    """
    # Combine title and description for analysis
    combined_text = f"{article.get('title', '')} {article.get('description', '')}"
    
    sentiment_score = calculate_sentiment_score(combined_text)
    
    # Categorize sentiment
    if sentiment_score >= 0.2:
        sentiment = "positive"
    elif sentiment_score <= -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {
        **article,
        "sentiment": sentiment,
        "sentiment_score": round(sentiment_score, 3)
    }


def analyze_articles(articles: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Analyze sentiment for multiple articles."""
    return [analyze_article(article) for article in articles]


def load_processed_news(file_path: Path) -> List[Dict[str, str]]:
    """Load processed articles from JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_analysis_results(file_path: Path, results: List[Dict[str, Any]]) -> None:
    """Save analysis results to JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    """Analyze sentiment for all processed news files."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    if not PROCESSED_DATA_DIR.exists():
        print(f"Processed data directory not found: {PROCESSED_DATA_DIR}")
        return
    
    processed_files = sorted(PROCESSED_DATA_DIR.glob("processed_*.json"))
    
    for processed_file in processed_files:
        print(f"Analyzing {processed_file.name}...")
        articles = load_processed_news(processed_file)
        analyzed = analyze_articles(articles)
        
        output_file = RESULTS_DIR / f"sentiment_{processed_file.stem}.json"
        save_analysis_results(output_file, analyzed)
        
        # Print summary statistics
        sentiments = [a["sentiment"] for a in analyzed]
        print(f"  Results: Positive={sentiments.count('positive')}, "
              f"Neutral={sentiments.count('neutral')}, "
              f"Negative={sentiments.count('negative')}")
        print(f"  Saved to {output_file.name}")


if __name__ == "__main__":
    main()

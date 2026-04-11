import os
import csv
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from configM.stocks import STOCKS #type: ignore

RAW_DATA_DIR = BASE_DIR / "dataM" / "raw" / "csv"
API_ENDPOINT = "https://newsapi.org/v2/everything"

DEFAULT_TIME_WINDOWS = [1, 5, 10, 15, 20, 25, 30]


def fetch_news(stock, api_key, days=30, sleep_duration=1):
    """Fetch and save news articles for a stock over specified days."""
    window_dir = RAW_DATA_DIR / f"{days}_days"
    window_dir.mkdir(parents=True, exist_ok=True)
    
    to_dt = datetime.now(timezone.utc)
    from_dt = to_dt - timedelta(days=days)
    date_range = (from_dt.strftime("%Y-%m-%dT%H:%M:%S"), to_dt.strftime("%Y-%m-%dT%H:%M:%S"))
    
    query = f'("{stock["name"]}" OR "{stock["ticker"]}") AND (stock OR market OR earnings OR finance)'
    stock_name = f'{stock["ticker"]}_{stock["name"]}'.lower().replace(" ", "_")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    
    try:
        page = 1
        r = requests.get(
            API_ENDPOINT,
            params={
                "q": query,
                "from": date_range[0],
                "to": date_range[1],
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 100,
                "page": page,
                "apiKey": api_key,
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        
        articles = data.get("articles", [])
        if not articles:
            print(f"    ℹ  No articles found")
        else:
            path = window_dir / f"news_{stock_name}_{ts}_p{page}.csv"
            
            fieldnames = [
                "source_name", "author", "title", "description", "url",
                "url_to_image", "published_at", "content"
            ]
            
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for article in articles:
                    row = {
                        "source_name": article.get("source", {}).get("name", ""),
                        "author": article.get("author", ""),
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "url": article.get("url", ""),
                        "url_to_image": article.get("urlToImage", ""),
                        "published_at": article.get("publishedAt", ""),
                        "content": article.get("content", ""),
                    }
                    writer.writerow(row)
            
            print(f"    ✓ {days}d: {len(articles)} articles")
        
        time.sleep(sleep_duration)
    except requests.exceptions.HTTPError as e:
        print(f"    ✗ {days}d: HTTP Error {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"    ✗ {days}d: Request Error - {e}")
    except Exception as e:
        print(f"    ✗ {days}d: Error - {e}")


def main():
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise RuntimeError("Set NEWS_API_KEY environment variable")
    
    sleep_duration = int(os.getenv("NEWS_API_SLEEP", "1"))
    
    time_windows_str = os.getenv("TIME_WINDOWS", "1,5,10,15,20,25,30")
    time_windows = [int(x.strip()) for x in time_windows_str.split(",")]
    
    print("\n📰 Fetching news for all sectors and time windows...\n")
    for sector, stocks in STOCKS.items():
        print(f"🏢 {sector.upper()}")
        for stock_data in stocks:
            stock = {"sector": sector, "ticker": stock_data["ticker"], "name": stock_data["name"]}
            print(f"  {stock['ticker']:5} | {stock['name']:15}")
            for days in time_windows:
                fetch_news(stock, api_key, days, sleep_duration)
    
    print("\n✓ Fetch complete!\n")


if __name__ == "__main__":
    main()
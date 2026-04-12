# News Sentiment Analysis
## Project Structure

```
martin-news-sentiment/
├── srcM/                          # Source code
│   ├── data/
│   │   ├── fetch_news.py         # Fetch news from NewsAPI
│   │   └── preprocess_news.py    # Preprocess raw articles
│   └── sentiment/
│       └── rule_based.py         # Rule-based sentiment analysis
├── configM/
│   └── stocks.py                 # Stock configuration (8 sectors)
├── dataM/
│   ├── raw/                      # Raw CSV responses from API
│   ├── interim/                  # Intermediate data files
│   └── processed/                # Preprocessed articles
├── resultsM/                      # Sentiment analysis results
├── experimentsM/                  # Experimental notebooks/scripts
└── requirements.txt              # Python dependencies
```




STOCKS = {
    "technology": [
        {"ticker": "AAPL", "name": "Apple"},
        {"ticker": "MSFT", "name": "Microsoft"},
        {"ticker": "GOOGL", "name": "Alphabet"},
        {"ticker": "AMZN", "name": "Amazon"},
        {"ticker": "META", "name": "Meta"},
        {"ticker": "NVDA", "name": "Nvidia"},
        {"ticker": "AMD", "name": "AMD"},
        {"ticker": "TSM", "name": "TSMC"},
    ],
    "semiconductors": [
        {"ticker": "AVGO", "name": "Broadcom"},
        {"ticker": "QCOM", "name": "Qualcomm"},
        {"ticker": "INTC", "name": "Intel"},
    ],
    "ai_software": [
        {"ticker": "PLTR", "name": "Palantir"},
        {"ticker": "CRM", "name": "Salesforce"},
        {"ticker": "ORCL", "name": "Oracle"},
        {"ticker": "IBM", "name": "IBM"},
    ],
    "defense": [
        {"ticker": "LMT", "name": "Lockheed Martin"},
        {"ticker": "RTX", "name": "RTX"},
        {"ticker": "NOC", "name": "Northrop Grumman"},
        {"ticker": "GD", "name": "General Dynamics"},
    ],
    "energy": [
        {"ticker": "XOM", "name": "Exxon Mobil"},
        {"ticker": "CVX", "name": "Chevron"},
        {"ticker": "COP", "name": "ConocoPhillips"},
        {"ticker": "SLB", "name": "Schlumberger"},
    ],
    "finance": [
        {"ticker": "JPM", "name": "JPMorgan"},
        {"ticker": "GS", "name": "Goldman Sachs"},
        {"ticker": "BAC", "name": "Bank of America"},
        {"ticker": "MS", "name": "Morgan Stanley"},
    ],
    "healthcare": [
        {"ticker": "LLY", "name": "Eli Lilly"},
        {"ticker": "JNJ", "name": "Johnson & Johnson"},
        {"ticker": "PFE", "name": "Pfizer"},
        {"ticker": "MRK", "name": "Merck"},
    ],
    "industrials": [
        {"ticker": "CAT", "name": "Caterpillar"},
        {"ticker": "GE", "name": "GE Aerospace"},
        {"ticker": "HON", "name": "Honeywell"},
    ],
    "consumer": [
        {"ticker": "TSLA", "name": "Tesla"},
        {"ticker": "WMT", "name": "Walmart"},
        {"ticker": "MCD", "name": "McDonald's"},
    ],
    "real_estate": [
        {"ticker": "PLD", "name": "Prologis"},
        {"ticker": "VICI", "name": "VICI Properties"},
    ],
    "utilities": [
        {"ticker": "NEE", "name": "NextEra Energy"},
        {"ticker": "SO", "name": "Southern Company"},
    ],
    "materials": [
        {"ticker": "NEM", "name": "Newmont"},
        {"ticker": "FCX", "name": "Freeport-McMoRan"},
    ]
}
POSITIVE_WORDS = {
    "beat", "beats", "growth", "surge", "strong", "stronger", "gain", "gains",
    "bullish", "upgrade", "outperform", "record", "profit", "profits", "expands",
    "partnership", "launch", "winner", "optimistic", "improved", "rise", "rises"
}

NEGATIVE_WORDS = {
    "miss", "misses", "weak", "weaker", "fall", "falls", "drop", "drops",
    "bearish", "downgrade", "underperform", "loss", "losses", "lawsuit", "risk",
    "warns", "warning", "cut", "cuts", "decline", "declines", "concern", "concerns"
}
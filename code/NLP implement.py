import feedparser
# Use a pipeline as a high-level helper
from transformers import pipeline
ticker='MSFT'
keyword='microsoft'

pipe = pipeline("text-classification", model="ProsusAI/finbert")

rss_url= f'https://finance.yahoo.com/rss/headline?s={ticker}'
feed= feedparser.parse(rss_url)
######
total_score =0
most_relevant=""
articles=0
total_positive=0
total_negative=0
overall_sentiment=""
threshhold1=0.2
threshhold2=-0.2
#######

for i,entry in enumerate(feed.entries) :
    if  keyword.lower()not in entry.summary.lower() :
        continue
    else:
        print(f'Title: {entry.title}')
        #print(f'date: {entry.published}')
        #print(f'link: {entry.link}')
        sentiment=pipe(entry.summary)[0]
        print(f"score is : {sentiment['score']}")
        sentiment_score = 0
        if sentiment["label"]=="positive":
            sentiment_score = sentiment['score']
            total_score+=sentiment_score
            total_positive+=1
            print("this is positive ")
        elif sentiment["label"]=="negative":
            sentiment_score = -sentiment['score']
            total_score+=sentiment_score
            total_negative+=1
            print("this is negative")
        else:
            continue

        articles +=1
if articles==0:
    print("0 articles")
else:
    final_score=total_score/articles
if final_score> threshhold1 :
    overall_sentiment='positive'
elif final_score<threshhold2:
    overall_sentiment='negative'
else:
    overall_sentiment='neutral'
largest_difference=0
for i,entry in enumerate(feed.entries) :
    sentiment = pipe(entry.title)[0]
    sentiment_score = sentiment['score']
    sentiment_label = sentiment['label']
    difference = abs(final_score - sentiment_score)
    
    if difference > largest_difference:
        largest_difference = difference
        most_relevant = entry.link
        
print (f"the total score is {round(final_score,2)} and the overall sentiment is {overall_sentiment}")
print (f"toal articles: {articles}")
print (f"toal number of positive articles: {total_positive}")
print (f"toal number of negative articles: {total_negative}")
print(f"the most relevant article is : {most_relevant} ")

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def plot_sentiment_meter(final_score):
    """
    Create a meter showing sentiment score between -1 and 1
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 2))
    
    # Define the meter parameters
    meter_width = 10
    meter_height = 1
    
    # Create color gradient from red to yellow to green
    colors = ['red', 'white', 'green']
    cmap = LinearSegmentedColormap.from_list('sentiment', colors, N=100)
    
    # Draw the gradient background
    for i in range(100):
        x = -1 + (i / 100) * 2  # Map from -1 to 1
        # Convert x to position on meter (0 to meter_width)
        pos_x = (x + 1) / 2 * meter_width
        
        color = cmap((x + 1) / 2)  # Normalize to 0-1 for colormap
        rect = patches.Rectangle(
            (pos_x, 0), 
            meter_width / 100, 
            meter_height, 
            facecolor=color, 
            edgecolor='none'
        )
        ax.add_patch(rect)
    
    # Add a pointer/marker for the final_score
    pointer_x = (final_score + 1) / 2 * meter_width
    ax.scatter(pointer_x, meter_height/2, color='black', s=200, zorder=5, marker='v')
    ax.scatter(pointer_x, meter_height/2, color='white', s=80, zorder=6, marker='v')
    
    # Add text for the score
    ax.text(pointer_x, meter_height + 0.2, f'{final_score:.3f}', 
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Add labels
    ax.text(0, -0.2, 'Negative (-1)', ha='left', va='top', fontsize=10)
    ax.text(meter_width/2, -0.2, 'Neutral (0)', ha='center', va='top', fontsize=10)
    ax.text(meter_width, -0.2, 'Positive (1)', ha='right', va='top', fontsize=10)
    
    # Add sentiment label
    if final_score < -0.5:
        sentiment = "Strongly Negative"
        color = 'red'
    elif final_score < -0.2:
        sentiment = "Negative"
        color = 'darkred'
    elif final_score < 0.2:
        sentiment = "Neutral"
        color = 'gray'
    elif final_score < 0.5:
        sentiment = "Positive"
        color = 'darkgreen'
    else:
        sentiment = "Strongly Positive"
        color = 'green'
    
    ax.text(meter_width/2, meter_height + 0.6, f'Sentiment: {sentiment}', 
            ha='center', fontsize=14, fontweight='bold', color=color)
    
    # Set axis limits and remove ticks
    ax.set_xlim(0, meter_width)
    ax.set_ylim(-0.5, meter_height + 0.8)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add title
    ax.set_title('Sentiment Analysis Meter', fontsize=16, pad=20)
    
    plt.tight_layout()
    plt.savefig(f"result {ticker}.png")
    plt.show()
    

plot_sentiment_meter(final_score)





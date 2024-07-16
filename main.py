import requests
from bs4 import BeautifulSoup
import schedule
import time
import json
import os
from datetime import datetime, timedelta
from google.generativeai import GenerativeModel, configure
from dotenv import load_dotenv
from Sentiment import SentOriginal  # Import the sentiment analysis function

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    configure(api_key=api_key)
    model = GenerativeModel('gemini-1.5-flash')
else:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
    exit(1)

# Function to parse relative time strings into datetime objects
def parse_relative_time(time_str):
    current_time = datetime.now()
    if 'hour' in time_str:
        hours_ago = int(time_str.split()[0])
        return current_time - timedelta(hours=hours_ago)
    elif 'minute' in time_str:
        minutes_ago = int(time_str.split()[0])
        return current_time - timedelta(minutes_ago)
    elif 'day' in time_str:
        days_ago = int(time_str.split()[0])
        return current_time - timedelta(days_ago)
    else:
        return current_time

# Function to scrape tech news
def scrape_tech_news():
    url = 'https://www.techcrunch.com'  # Replace with the actual tech news website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    data_file = 'tech_news.json'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example for extracting news titles and links
        articles = soup.find_all('div', class_='wp-block-tc23-post-picker')  # Modify based on website's structure
        news_list = []
        for article in articles:
            title_tag = article.find('h2')
            if title_tag:
                title = title_tag.text
                link = title_tag.find('a')['href']
                time_tag = article.find("time", class_='wp-block-tc23-post-time-ago')
                if time_tag:
                    time_str = time_tag.text.strip()
                    time_posted = parse_relative_time(time_str)
                    
                    news_item = {
                        'title': title,
                        'link': link,
                        'timeposted': time_posted.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    news_list.append(news_item)

        # Only keep articles within the last 5 hours
        five_hours_ago = datetime.now() - timedelta(hours=24)
        news_list = [article for article in news_list if datetime.strptime(article['timeposted'], '%Y-%m-%d %H:%M:%S') > five_hours_ago]

        # Save the data to JSON file, replacing the old data
        with open(data_file, 'w') as file:
            json.dump(news_list, file, indent=4)

        print(f'Scraped {len(news_list)} articles and saved to {data_file}.')

    except requests.exceptions.RequestException as e:
        print(f'Error fetching the webpage: {e}')

# Function to scrape article details from the links in the JSON file
def scrape_article_details():
    data_file = 'tech_news.json'
    article_details_file = 'article_details.json'
    
    if not os.path.exists(data_file):
        print(f'{data_file} does not exist.')
        return

    with open(data_file, 'r') as file:
        news_list = json.load(file)

    detailed_articles = []

    for news_item in news_list:
        try:
            response = requests.get(news_item['link'])
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Example of scraping the article details
            category = soup.find('a', class_='is-taxonomy-category wp-block-tenup-post-primary-term')
            article_content = soup.find('div', class_='wp-block-post-content')  # Modify based on website's structure
            content = article_content.get_text(strip=True) if article_content else "No content found"

            try:
                paraphrased_title = model.generate_content(f"Paraphrase the following title and return a single paraphrased title with no additional information: {news_item['title']}").text
                paraphrased_content = model.generate_content(f"Paraphrase the following content and return the paraphrased content in a markup format: {content}").text
            except Exception as e:
                print(f'Error using Google Generative AI for paraphrasing: {e}')
                paraphrased_title = news_item['title']
                paraphrased_content = content

            # Perform sentiment analysis on the paraphrased content
            sentiment_analysis = SentOriginal(paraphrased_content)

            detailed_article = {
                'original_title': news_item['title'],
                'paraphrased_title': paraphrased_title,
                'category': category.get_text(strip=True) if category else 'No category',
                'timeposted': news_item['timeposted'],
                'original_content': content,
                'paraphrased_content': paraphrased_content,
                'sentiment_analysis': sentiment_analysis  # Add sentiment analysis result
            }

            detailed_articles.append(detailed_article)
            print(f'Scraped and paraphrased details for article: {news_item["title"]}')

        except requests.exceptions.RequestException as e:
            print(f'Error fetching the article page: {e}')

    # Save the detailed articles to JSON file
    with open(article_details_file, 'w') as file:
        json.dump(detailed_articles, file, indent=4)

    print(f'Scraped and paraphrased details of {len(detailed_articles)} articles and saved to {article_details_file}.')

# Schedule the scraping functions
schedule.every(5).hours.do(scrape_tech_news)
schedule.every(5).hours.do(scrape_article_details)

# Initial runs
scrape_tech_news()
scrape_article_details()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

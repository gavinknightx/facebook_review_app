import requests
from datetime import datetime, timedelta
import json

# Gets the access token and ID for the given company
def retrieve_access_tokens(company_name):
    with open('config/tokens.json', 'r') as file:
        all_reviews = json.load(file)

    for company in data['data']:
        if company['name'].lower() == company_name.lower():
            return company['access_token'],company['id']

# Gets real Facebook reviews using the Facebook API
def fetch_facebook_reviews_real(company_name):

    ACCESS_TOKEN, PAGE_ID = retrieve_access_tokens(company_name)

    url = f'https://graph.facebook.com/v21.0/{PAGE_ID}/ratings'
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'rating,review_text,created_time'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        reviews_data = response.json()
        reviews = reviews_data.get('data', [])

        print(reviews)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# Gets dummy review data from a local json
def fetch_facebook_reviews_dummy(company_name):
    with open('data/reviews.json', 'r') as file:
        all_reviews = json.load(file)
    
    return all_reviews[company_name]

# Filter the reviews by:
# - Only keeping reviews from last 6 months
# - Only keeping reviews with both rating and text
# - Sorting them by date
# - Limiting to 100 reviews
def filter_reviews(reviews):
    if not reviews:
        return []

    today = datetime.now(datetime.strptime(reviews[0]['created_time'], '%Y-%m-%dT%H:%M:%S%z').tzinfo)
    six_months_ago = today - timedelta(days=180)

    filtered_reviews = []

    for review in reviews:
        review_date = datetime.strptime(review['created_time'], '%Y-%m-%dT%H:%M:%S%z')
        
        if review_date >= six_months_ago:
            if 'rating' in review and ('review_text' in review and review['review_text'] != ''):
                filtered_reviews.append(review)
    
    filtered_reviews.sort(key=lambda x: datetime.strptime(x['created_time'], '%Y-%m-%dT%H:%M:%S%z'), reverse=True)
    
    return filtered_reviews[:100]

# main function to retrieve and filter review data
def fetch_filtered_reviews(company_name):
    return filter_reviews(fetch_facebook_reviews_dummy(company_name))
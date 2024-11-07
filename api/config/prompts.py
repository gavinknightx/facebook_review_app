
from fb_reviews import fetch_filtered_reviews

SYSTEM_PROMPT = """
You are a Social Media review analyst. Extract meaningful information such as company name from the user interaction. 
If the company name is not available as a tool call parameter say its not available in the list. Execute the instructions given by the user.
"""

def create_review_prompt(company_name):

    reviews = fetch_filtered_reviews(company_name)
        
    review_texts = [f"Rating: {review['rating']}\nReview: {review['review_text']}" for review in reviews]

    average_rating = round(sum(r['rating'] for r in reviews) / len(reviews),2)

    print(average_rating)

    total_reviews = len(reviews)

    print(company_name)

    # Create prompt for LLM
    review_prompt = f"""Analyze these {len(reviews)} company facebook reviews and identify the top 3 unique sentiment categories.
    For each category, determine the overall sentiment (positive/negative/neutral), 
    confidence score (0-100), common themes, and provide a representative example review.

    do not change any of the following values in final output.
    Total Reviews: {total_reviews}
    Average Rating : {average_rating}
    Company Name : {company_name}

    Reviews:
    {review_texts}

    Output the analysis in this exact format:
    {{"company_name": <company name>,
      "total_reviews": int,
      "average_rating": float,
        "top_sentiments": [
            {{
                "category": "<category name>",
                "sentiment": "<positive/negative/neutral>",
                "confidence": <0-100>,
                "themes": ["theme1", "theme2"],
                "example_review": "<exact review text>"
            }}
        ]
    }}
    """

    return review_prompt, total_reviews, average_rating

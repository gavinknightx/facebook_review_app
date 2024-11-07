import openai
from dotenv import load_dotenv
from os import getenv
import json
from config.prompts import create_review_prompt, SYSTEM_PROMPT
from pydantic import BaseModel
from typing import List

load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

if openai.api_key is None:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

class SentimentModel(BaseModel):
    category: str
    sentiment: List[str] 
    confidence: int 
    themes: List[str]
    example_review: str

class TopSentimentsModel(BaseModel):
    company_name:str
    total_reviews:int
    average_rating:float
    top_sentiments:List[SentimentModel]

company_mapping = {
    'dialog' : "Dialog",
    'slt':'SLT',
    'elephant_house':"Elephant House"
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_facebook_reviews",
            "description": "Fetch Facebook ratings for the a given company",
            "parameters":{
                "type":"object",
                "properties":{
                    "company_name":{
                        "type":"string",
                        "description" : "the company name",
                        "enum" : ["dialog", "slt", "elephant_house"]
                    }
                }
            }
        }
    }
]


# Takes the analyzed review data and formats it into a readable message
# Returns a string with company stats and top 3 sentiments formatted nicely
def create_review_display_message(data):

    print(data)

    star_rating = "⭐" * round(data["average_rating"])
    message = f"Based on {company_mapping[data['company_name']]}'s Facebook reviews, here are the top 3 sentiments:\n\n"

    for i, sentiment in enumerate(data["top_sentiments"], 1):
        message += f"{i}. {sentiment['category'].title()}\n\n"
        message += f"Sentiment: {sentiment['sentiment'][0].capitalize()} ({sentiment['confidence']}% confidence)\n\n"
        message += f"Common themes: {', '.join(sentiment['themes'])}\n\n"
        message += f"Example review: \"{sentiment['example_review']}\"\n\n\n"
    
    message += f"Average rating: {star_rating} ({data['average_rating']}/5) from {data['total_reviews']} reviews\n\n"
    message += "Would you like to analyze another company?"

    return message

# Main function that handles sentiment analysis using OpenAI
# Makes tool calls to fetch reviews and parse them into structured data
def analyze(request):
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        messages.extend([msg.dict() for msg in request.messages])

        # Make initial API call to get tool calls
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        # Check if we got a tool call back
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            arguments = json.loads(tool_call.function.arguments)
            company_name = arguments['company_name']

            # Get review data and create prompt
            review_prompt, total_reviews, average_rating = create_review_prompt(company_name)

            function_call_result_message = {
                "role": "tool",
                "content": company_name,
                "tool_call_id": response.choices[0].message.tool_calls[0].id
            }

            # Add assistant response, tool result, and review prompt to messages
            messages.append(response.choices[0].message)
            messages.append(function_call_result_message)
            messages.append({"role": "user", "content": review_prompt})

            # Make second API call to get review response as structured output
            response = openai.beta.chat.completions.parse(
                model="gpt-4o",
                messages=messages,
                response_format=TopSentimentsModel
            )

            # Format final output message
            output_message = create_review_display_message(json.loads(response.choices[0].message.content))

            return {"message": output_message}
        else:
            # If no tool call needed, return direct response
            print("no tool call invoked")
            return {"message": response.choices[0].message.content}

    except Exception as e:
        # Handle any exceptions and provide an error message
        print(f"Error occurred: {e}")
        return {"message": f"An error occurred: {e}"}
import os
import requests
import pandas as pd
from time import sleep

# Function to fetch questions from the API with pagination
def fetch_all_questions(api_url, limit=100):
    all_questions = []
    offset = 0
    while True:
        response = requests.get(f'{api_url}?limit={limit}&offset={offset}')
        if response.status_code == 429:
            print("Error 429: Too Many Requests. Retrying after a delay...")
            sleep(60)  # Wait for 60 seconds before retrying
            continue
        elif response.status_code != 200:
            print(f'Error: {response.status_code}')
            break
        data = response.json()
        questions = data.get('problemsetQuestionList', [])
        if not questions:
            break
        all_questions.extend(questions)
        offset += limit
    return all_questions

# Function to parse and process the API response
def process_api_response(questions):
    question_list = []
    for question in questions:
        question_data = {
            'title': question.get('title'),
            'difficulty': question.get('difficulty'),
            'acRate': question.get('acRate'),
            'status': question.get('status'),
            'topicTags': [tag['name'] for tag in question.get('topicTags', [])]
        }
        question_list.append(question_data)
    return question_list

# Set the API endpoint
api_url = 'https://alfa-leetcode-api.onrender.com/problems'

# Fetch all questions
all_questions = fetch_all_questions(api_url)

# Process the API response
question_data = process_api_response(all_questions)
df = pd.DataFrame(question_data)

# File path
file_path = 'leetcode_problems.csv'

# Check if file exists
if not os.path.exists(file_path):
    # If file doesn't exist, save the data
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")
else:
    # If file exists, compare file sizes
    current_size = len(df)
    existing_df = pd.read_csv(file_path)
    existing_size = len(existing_df)
    
    if current_size > existing_size:
        # Save only if current data is not smaller
        df.to_csv(file_path, index=False)
        print(f"Data updated in {file_path}")
    else:
        print(f"Current data has fewer entries than existing file. Data not saved.")
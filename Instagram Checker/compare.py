import re
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
from itertools import zip_longest

def parse_instagram_file(html_content):
    """Parse Instagram HTML file for usernames and dates"""
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []
    
    user_divs = soup.find_all('div', class_='_a6-p')
    
    for div in user_divs:
        username_elem = div.find('a')
        date_elem = div.find_all('div')[-1]
        
        if username_elem and date_elem:
            username = username_elem.text.strip()
            date = date_elem.text.strip()
            data.append((username, date))
    
    return data

def process_file(file_path):
    """Process a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            parsed_data = parse_instagram_file(html_content)
            return [item[0] for item in parsed_data]  # Return only usernames
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
    return []

def compare_and_save(following_usernames, followers_usernames, output_path):
    """Compare usernames and save results to CSV"""
    following_only = set(following_usernames) - set(followers_usernames)
    followers_only = set(followers_usernames) - set(following_usernames)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Following Only', 'Followers Only'])
        writer.writerows(zip_longest(following_only, followers_only, fillvalue=''))
    
    print(f"Comparison results saved to {output_path}")

# Main processing
if __name__ == "__main__":
    # Define the Instagram data directory
    instagram_data_dir = './connections/followers_and_following'
    
    # Default filenames for following and followers HTML files
    default_filenames = {
        'following': 'following.html',
        'followers': 'followers_1.html'
    }
    
    # Process following file
    following_path = os.path.join(instagram_data_dir, default_filenames['following'])
    following_usernames = process_file(following_path)
    
    # Process followers file
    followers_path = os.path.join(instagram_data_dir, default_filenames['followers'])
    followers_usernames = process_file(followers_path)
    
    # Compare and save results
    output_path = os.path.join(os.getcwd(), 'ig_comparison.csv')
    compare_and_save(following_usernames, followers_usernames, output_path)

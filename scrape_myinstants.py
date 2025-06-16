# scrape_myinstants.py

import requests
from bs4 import BeautifulSoup
import os
import time
import re

# --- Configuration ---
# The URL for the Indian trending page on MyInstants
TARGET_URL = "https://www.myinstants.com/en/index/in/"
BASE_URL = "https://www.myinstants.com"

# Where to save the downloaded sounds. This should match your main project's sound folder.
SAVE_FOLDER = "sounds"
# --- End Configuration ---

def clean_filename(name):
    """Cleans a string to be a valid filename."""
    name = name.lower()  # Convert to lowercase
    name = re.sub(r'[^\w\s-]', '', name).strip() # Remove special characters except words, spaces, hyphens
    name = re.sub(r'[-\s]+', '_', name) # Replace spaces and hyphens with underscores
    return name + ".mp3"

def scrape_myinstants():
    """
    Scrapes the MyInstants website for sound clips, downloads them,
    and saves them with clean filenames.
    """
    print(f"--- 🎵 Starting Scraper for MyInstants ---")
    print(f"Target URL: {TARGET_URL}")

    # Create the save folder if it doesn't already exist
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"Created directory: {SAVE_FOLDER}")

    # Use headers to mimic a real web browser, which can help avoid getting blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # Step 1: Get the webpage content
        response = requests.get(TARGET_URL, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (like 404 or 500)
        
        # Step 2: Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Step 3: Find all the individual sound containers
        instants = soup.find_all('div', class_='instant')
        
        if not instants:
            print("Could not find any instants on the page. The website structure might have changed.")
            return

        print(f"Found {len(instants)} sound clips on the page. Starting download...")
        
        for instant in instants:
            # Find the button to extract the sound URL
            button = instant.find('button', class_='small-button')
            # Find the link to extract the sound name
            link = instant.find('a', class_='instant-link')
            
            if button and link:
                # Extract the 'onclick' attribute string
                onclick_attr = button.get('onclick', '')
                
                # Use a regular expression to reliably extract the sound path
                match = re.search(r"play\('([^']*)'", onclick_attr)
                
                if match:
                    relative_audio_url = match.group(1)
                    full_audio_url = BASE_URL + relative_audio_url
                    
                    # Get the sound name and create a clean filename
                    sound_name = link.text.strip()
                    filename = clean_filename(sound_name)
                    filepath = os.path.join(SAVE_FOLDER, filename)
                    
                    # --- Download Logic ---
                    # Check if the file already exists to avoid re-downloading
                    if not os.path.exists(filepath):
                        print(f"  -> Downloading '{sound_name}' to '{filename}'...")
                        try:
                            audio_response = requests.get(full_audio_url, headers=headers, timeout=10)
                            audio_response.raise_for_status()
                            
                            with open(filepath, 'wb') as f:
                                f.write(audio_response.content)
                            
                            # Be a good citizen and don't spam the server with requests
                            time.sleep(0.5) 
                        except requests.exceptions.RequestException as e:
                            print(f"     ERROR: Failed to download {sound_name}. Reason: {e}")
                    else:
                        print(f"  -> Skipping '{filename}' (already exists).")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not retrieve the webpage. Reason: {e}")

    print("\n--- ✅ Scraping complete! ---")
    print(f"Check the '{SAVE_FOLDER}' directory for your Indian meme sounds.")

if __name__ == "__main__":
    scrape_myinstants()
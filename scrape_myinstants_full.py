# scrape_myinstants_efficient.py

import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# --- Configuration ---
TARGET_URL = "https://www.myinstants.com/en/index/in/"
BASE_URL = "https://www.myinstants.com"
SAVE_FOLDER = "sounds"
SCROLL_PAUSE_TIME = 2  # Time to wait after each scroll
# --- End Configuration ---

def clean_filename(name):
    """Cleans a string to be a valid filename."""
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '_', name)
    return name + ".mp3"

def download_sound(session, url, filepath, sound_name):
    """Downloads a single sound file."""
    try:
        print(f"  -> Downloading '{sound_name}'...")
        audio_response = session.get(url, timeout=20)
        audio_response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(audio_response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"     ERROR: Failed to download {sound_name}. Reason: {e}")
        return False

def scrape_efficiently():
    """
    Scrapes MyInstants by progressively scrolling and downloading new content
    as it appears, which is much more efficient.
    """
    print("--- 🚀 Starting EFFICIENT Scraper for MyInstants ---")
    
    # Use a requests session for connection pooling
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    # Setup Selenium WebDriver
    print("Setting up Chrome WebDriver...")
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    except Exception as e:
        print(f"Error setting up automatic WebDriver: {e}")
        return

    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    # This set will store the URLs of sounds we've already processed
    processed_urls = set()

    try:
        print(f"Opening {TARGET_URL}...")
        driver.get(TARGET_URL)
        time.sleep(3)

        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Find all sound elements currently loaded in the DOM
            instants = driver.find_elements(By.CLASS_NAME, 'instant')
            new_sounds_found_in_pass = 0

            for instant in instants:
                try:
                    # Find the button to get the sound URL
                    button = instant.find_element(By.TAG_NAME, 'button')
                    onclick_attr = button.get_attribute('onclick')
                    
                    match = re.search(r"play\('([^']*)'", onclick_attr)
                    if not match:
                        continue

                    relative_audio_url = match.group(1)
                    full_audio_url = BASE_URL + relative_audio_url

                    # THE CORE LOGIC: Check if we've already processed this URL
                    if full_audio_url not in processed_urls:
                        # If it's new, process it
                        new_sounds_found_in_pass += 1
                        
                        # Add to the set immediately to mark it as processed
                        processed_urls.add(full_audio_url)
                        
                        # Get the name and create a clean filename
                        sound_name = instant.find_element(By.CLASS_NAME, 'instant-link').text.strip()
                        filename = clean_filename(sound_name)
                        filepath = os.path.join(SAVE_FOLDER, filename)
                        
                        if not os.path.exists(filepath):
                            download_sound(session, full_audio_url, filepath, sound_name)
                        else:
                            print(f"  -> Skipping '{filename}' (already exists).")

                except StaleElementReferenceException:
                    # This happens if the page re-renders while we're looping. Just continue.
                    continue
                except NoSuchElementException:
                    # Sometimes an 'instant' div might not have a button/link, skip it.
                    continue
            
            if new_sounds_found_in_pass > 0:
                 print(f"Processed {new_sounds_found_in_pass} new sounds in this pass. Total processed: {len(processed_urls)}")

            # Scroll down and wait
            print("\nScrolling for more sounds...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)

            # Check if we've reached the end
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the end of the page. No new content loaded.")
                break
            last_height = new_height
            
    finally:
        print("\nClosing the browser window.")
        driver.quit()

    print(f"\n--- ✅ EFFICIENT Scraping complete! ---")
    print(f"Total unique sounds downloaded: {len(processed_urls)}. Check the '{SAVE_FOLDER}' directory.")

if __name__ == "__main__":
    scrape_efficiently()
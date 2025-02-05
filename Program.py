import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Try importing the requests library
try:
    import requests
except ImportError:
    print("The 'requests' library is not installed. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# Try importing tqdm for progress bar
try:
    from tqdm import tqdm
except ImportError:
    print("The 'tqdm' library is not installed. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    from tqdm import tqdm

SCRYFALL_API = "https://api.scryfall.com/cards/named"

# Define the folder for downloaded files
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIRECTORY, "Downloaded Files")

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def sanitize_filename(filename):
    """
    Removes or replaces characters in the filename that are invalid for the OS.
    """
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

def parse_deck(deck_text):
    """
    Parses a decklist from the input text and returns a list of card dictionaries with their quantities.
    """
    deck = []
    lines = deck_text.strip().split("\n")
    for line in lines:
        if line.strip():  # Ignore empty lines
            try:
                quantity, *card_name = line.split(" ", 1)
                deck.append({"quantity": int(quantity), "name": card_name[0].strip()})
            except ValueError:
                print(f"{RED}Skipping invalid line (could not parse): {line}{RESET}")
    return deck

def download_card_image(card_name, output_dir, quantity=1):
    """
    Fetches the image URL from Scryfall and downloads the card image.
    """
    params = {"fuzzy": card_name}
    try:
        response = requests.get(SCRYFALL_API, params=params)
        response.raise_for_status()
        card_data = response.json()
        if "image_uris" not in card_data:
            return f"{RED}No image data available for {card_name}.{RESET}"
        
        image_url = card_data["image_uris"]["normal"]
        
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Save the images for the given quantity
        for i in range(1, quantity + 1):
            sanitized_name = sanitize_filename(f"{card_name}_copy{i}")
            file_name = os.path.join(output_dir, f"{sanitized_name}.jpg")
            with open(file_name, "wb") as f:
                f.write(image_response.content)
        
        return f"{GREEN}Downloaded: {card_name} (x{quantity}){RESET}"
    except requests.exceptions.RequestException as e:
        return f"{RED}Failed to download {card_name}: {e}{RESET}"

def save_deck(deck, output_dir):
    """
    Saves the parsed deck to a .txt file.
    """
    deck_file = os.path.join(output_dir, "downloaded_deck.txt")
    try:
        with open(deck_file, "w") as f:
            for card in deck:
                f.write(f"{card['quantity']} {card['name']}\n")
        print(f"{GREEN}Deck saved to {deck_file}{RESET}")
    except Exception as e:
        print(f"{RED}Failed to save deck: {e}{RESET}")

def main():
    try:
        if not os.path.exists(DEFAULT_OUTPUT_DIR):
            os.makedirs(DEFAULT_OUTPUT_DIR)
            print(f"Directory {DEFAULT_OUTPUT_DIR} created.")
        
        print("Paste your Archidekt deck text below and type DONE when you're finished:")
        deck_text = ""
        while True:
            line = input()
            if line.strip().upper() == "DONE":
                break
            deck_text += line + "\n"

        deck = parse_deck(deck_text)
        if deck:
            save_deck(deck, DEFAULT_OUTPUT_DIR)
            image_dir = os.path.join(DEFAULT_OUTPUT_DIR, "card_images")
            os.makedirs(image_dir, exist_ok=True)

            # Use multi-threading for downloads
            print("\nDownloading card images with multi-threading:")
            with ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(download_card_image, card["name"], image_dir, card["quantity"]): card
                    for card in deck
                }
                for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading"):
                    result = future.result()
                    if result:
                        print(result)
            print(f"\n{GREEN}All tasks completed successfully.{RESET}")
        else:
            print(f"{RED}No valid cards found in the input.{RESET}")
    except Exception as e:
        print(f"{RED}An unexpected error occurred: {e}{RESET}")
    
    input("\nProcessing complete. Press Enter to exit...")

if __name__ == "__main__":
    main()

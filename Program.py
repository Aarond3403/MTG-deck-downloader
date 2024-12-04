import os
import subprocess
import sys

# Try importing the requests library
try:
    import requests
except ImportError:
    # If requests is not installed, install it automatically
    print("The 'requests' library is not installed. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests  # Import again after installation

SCRYFALL_API = "https://api.scryfall.com/cards/named"

# Define the folder for downloaded files
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIRECTORY, "Downloaded Files")

# ANSI escape code for red text
RED = "\033[91m"
RESET = "\033[0m"

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
                print(f"{RED}Skipping invalid line: {line}{RESET}")
    return deck

def download_card_image(card_name, output_dir):
    """
    Fetches the image URL from Scryfall and downloads the card image.
    """
    params = {"fuzzy": card_name}
    try:
        response = requests.get(SCRYFALL_API, params=params)
        response.raise_for_status()
        card_data = response.json()
        image_url = card_data["image_uris"]["normal"]
        
        # Download the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Save the image
        file_name = os.path.join(output_dir, f"{card_name.replace(' ', '_')}.jpg")
        with open(file_name, "wb") as f:
            f.write(image_response.content)
        print(f"Downloaded: {card_name}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}Failed to download {card_name}: {e}{RESET}")

def save_deck(deck, output_dir):
    """
    Saves the parsed deck to a .txt file.
    """
    deck_file = os.path.join(output_dir, "downloaded_deck.txt")
    try:
        with open(deck_file, "w") as f:
            for card in deck:
                f.write(f"{card['quantity']} {card['name']}\n")
        print(f"Deck saved to {deck_file}")
    except Exception as e:
        print(f"{RED}Failed to save deck: {e}{RESET}")

def main():
    try:
        # Ensure the default output directory exists
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
            # Save deck list to the default directory
            save_deck(deck, DEFAULT_OUTPUT_DIR)

            # Create an output directory for images within the default location
            image_dir = os.path.join(DEFAULT_OUTPUT_DIR, "card_images")
            os.makedirs(image_dir, exist_ok=True)

            # Download images for each card
            for card in deck:
                download_card_image(card["name"], image_dir)
            print("\nAll tasks completed successfully.")
        else:
            print(f"{RED}No valid cards found in the input.{RESET}")
    except Exception as e:
        print(f"{RED}An error occurred: {e}{RESET}")
    
    input("\nProcessing complete. Press Enter to exit...")

if __name__ == "__main__":
    main()

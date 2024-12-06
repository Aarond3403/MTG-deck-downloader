# MTG Deck Image Downloader
This tool downloads Magic: The Gathering card images and saves the deck list as both image files and text files. It's designed to make sharing and printing your MTG decks easier!

## Requirements
Python 3.x (Download it from www.python.org/downloads/ if you don't have it installed)
Internet connection
## How to Use
## Step 1: Unzip the File
Extract all files from the provided .zip to a folder of your choice.

## Step 2: Run the Program
Find the file named Click Me.bat (in older versions, it’s called Click This Second) and run it as admin. It works without admin too, its just sometimes it breaks without.
Copy and paste your MTG deck list from Archidekt into the program.
IMPORTANT: When exporting from Archidekt, UNCHECK ALL OPTIONS
Add a new line to your deck list and type DONE, then press Enter. The program will begin downloading your cards and saving your deck. :D

## Step 3: Find Your Files
All images and deck files are saved in the Downloaded Files folder, which will be auto-generated in the program’s folder if everything works correctly.

## Troubleshooting
Issue: Errors About Missing Libraries (e.g., "requests")
If you see errors related to missing libraries (usually marked in red) like "requests," my auto-installer might have failed. Here’s how to fix it:

Open Command Prompt (search for "cmd") and run it as admin.
Type: pip install requests and press Enter.
The library will install, and the program should work.
Issue: Invalid Card or Deck Parsing Issues
If the program says something like invalid card:

Make sure you're using the correct export options in Archidekt. UNCHECK ALL OPTIONS like this:



Add a new line and type DONE before pressing Enter.

Testing the Program
If you’re unsure whether the program is broken or if you made a mistake, use the provided test deck file: test mtg friends to test it to see if it works.txt. Copy and paste its contents into the program to verify.

Issue: Missing Python
If you see errors related to Python not being installed, download it here: www.python.org/downloads/.

Credits
If my MTG Deck Downloader is too dumb, check out my friend’s version:
SuperiorTabby/MTG-Card-Printer

Happy deck building! :D


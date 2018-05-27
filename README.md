# WowAuctionTools
Tools for automating auction data retrieval using Blizzard API

# Installation & Setup
* Run "pip install -r requirements.txt"
* Copy config.py.example and name it config.py
* Enter a valid API key into config.py as well spreadsheet ID and data range (i.e. 'Item Data!A1:F400') if you want to use the spreadsheet feature.
* Head to https://console.developers.google.com/apis/credentials?project=wow-auction-tools-205308, download the OAuth JSON token and name it client_secret.json. Place it in the root folder of this project.

# Spreadsheet Format
Spreadsheet assumes the following column order:
Item ID, Name, Gold, Silver, Copper

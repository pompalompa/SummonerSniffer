# SummonerSniffer:
A project making use of OCR to track cool downs of summoner spells in League of Legends
## Prerequisites:
You need Tesseract-OCR installed. pip install pytesseract is not enough as that simply installs the library. You can 
find Tesseract-OCR here: https://github.com/tesseract-ocr
## Vars you Should Consider Tweaking:
### In SummonerSniffer.py:
#### TOP_LEFT_COORD:
A tuple that has the x,y coordinates of the top left corner of the chat window. Change based on monitor size and your 
chat position. DEFAULT = 20, 720.
#### BOTTOM_RIGHT_COORD:
A tuple that has the x,y coordinates of the bottom right corner of the chat window. Change based on monitor size and 
your chat position. DEFAULT = 700, 1355. 
#### REPORT_HOTKEY:
The key you want to run the program and generate a report. DEFAULT = '/ + .'
### In LeagueStuff.py:
#### pytesseract.pytesseract.tesseract_cmd:
This is wherever you installed Tesseract-OCR to. DEFAULT = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

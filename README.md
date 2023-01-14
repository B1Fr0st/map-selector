# map-selector
Uses OCR to only allowed selected maps on Modern Warfare 2

To use this, install the latest version of [python](https://www.python.org/downloads/release/python-3111/) (3.10+).

Currently, it has only been tested on Windows, so use on other platforms at your own risk.

Required modules:

pyautogui

pydirectinput

pytesseract

numpy

requests

pip command: ```pip install pyautogui pydirectinput pytesseract numpy requests```

You will also need the latest version of Tesseract x64, downloadable from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

Direct Download link: [tesseract-ocr-w32-setup-5.3.0.20221222.exe](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-5.3.0.20221222.exe)

Leave everything default, then go into your system environment variables, click on edit path, then add C:\Program Files(x86)\Tesseract-OCR to your path. This [site](https://ironsoftware.com/csharp/ocr/blog/ocr-tools/tesseract-ocr-windows/) does a good guide on install if you are stuck.

This also only has coordinates for 1920x1080 displays; if you have a 1440 or 4k display and can give coordinates, submit a pull request and I can approve it.

USAGE:

Open Modern Warfare 2 on the main screen, hovering over quick play. Start the program, and it will start matchmaking. Don't touch the mouse.

If it detects a map not on the approved list, it will back out of matchmaking and rejoin, effectively only giving you the maps you want.

Keep an eye on it; occasionally it will join a game in El Asilo immediately, and you will need to manually back out.

If this happens, just rejoin quick play, no need to restart the program.

Interfacing with myNotifier is enabled, simply remove the quotes at the end of the loop function and create a file called api-key.txt in the folder with the python file containing your myNotifier api-key, and voila! It will send a notification to your phone whenever a game is found with the map name included. The base plan of myNotifier is limited to 25 requests a month however, so only enable this if you don't mind using that up, or you have the unlimited plan.

REM Make sure to install pyinstaller with pip if you want to build your own binaries!
REM pip install pyinstaller

pyinstaller main.py --noconfirm --onefile --name "musical-images-generator"

$env:PYTHONPATH=".\src"
pyinstaller --onefile --add-data "models:models" .\src\main.py

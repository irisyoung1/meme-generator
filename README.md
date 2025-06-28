# Meme Generator

This project generates meme images from quotes and photos, with both a command-line and a web interface.

## Requirements
- Python 3.13+
- pip

## Setup
1. **Download/ Clone project**
2. **Create and activate a virtual environment (recommended):**
   ```sh
   python -m venv .env-meme-gen
   # On Windows:
   .env-meme-gen\Scripts\activate
   # On macOS/Linux:
   source .env-meme-gen/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Running the App

### Command Line
Generate a meme from the command line:
```sh
python src/meme.py
```
This will output the path to a generated meme image.

### Web App
Start the web server:
```sh
python src/app.py
```
Then open your browser and follow the running port. In my case it is [http://localhost:5000](http://localhost:5000) or [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Linting and Testing
- **Lint code and docstrings:**
  ```sh
  pip install flake8 flake8-docstrings
  flake8
  ```
- **Run tests:**
  ```sh
  pytest
  ```

## Notes
- All dependencies are listed in `requirements.txt` (exported with `pip freeze`).
- For PDF quote extraction, no external binaries are required (uses pure Python `pdfminer.six`).
- For Windows users, all features work natively.

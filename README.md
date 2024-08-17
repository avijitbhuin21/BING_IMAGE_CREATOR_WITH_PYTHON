# BING_IMAGE_CREATOR_WITH_PYTHON
programmatically using the bing image creator

Example Use:
import json
from Bing_Image_Generator import Image_Gen
data = json.load(open("templates\cookies.json")) <-- loading cookies from "cookies.json" file**
image_generator = Image_Gen(all_cookies=data)
res=image_generator.Generate(prompt=prompt)
return res <-- it will return a list of four links containing the pictures.


** to get cookies.json install cookie editor in your browser. Open bing and login. click on the cookie editor and export as a JSON file.


#MASS IMAGE GENERATOR:

This Python script automates the generation and download of images using the Bing Image Creator. It uses cookies and headers to mimic browser behavior and handles multiple concurrent requests.

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.x** installed on your system.
2. **Google Colab**: The script is designed to run in a Colab environment.
3. **Browser Cookies**: Obtain cookies from a logged-in session on Bing.com and save them as JSON files. You'll need separate cookie files for each user.

### Python Libraries

The following Python libraries are required:

- `requests`
- `beautifulsoup4`
- `re`
- `time`
- `json`
- `random`
- `os`
- `concurrent.futures`

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Installation

1. **Clone the repository** or copy the script into your Colab environment.

2. **Upload your cookie JSON files** to Google Drive. Place them in a directory (e.g., `/content/drive/MyDrive/Cookies/`).

3. **Configure your Google Drive** in Colab:

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

## Usage

1. **Instantiate the Bing Image Generator**:

   ```python
   ethan = Bing_Image_Gen("/content/drive/MyDrive/Cookies/ethan.json")
   ```

   Repeat for other users as needed (e.g., mason, amelia, alexander).

2. **Generate Images**:

   Use the `Generate` method to create images based on a given prompt.

   ```python
   ethan.Generate("a futuristic cityscape", "ethan_city")
   ```

   This will create and save images to Google Drive under `/content/drive/MyDrive/Unchecked/`.

## Script Breakdown

### `Bing_Image_Gen` Class

- **`__init__(self, cookie_path)`**: Initializes the session with cookies and headers for a user.

- **`start_generation_sequence(self, url_encoded_prompt, name)`**: Initiates the image generation process on Bing.

- **`get_download_links(self, url, name)`**: Polls Bing until the images are ready and extracts download links.

- **`Generate(self, prompt: str, name: str)`**: Combines the steps to create images and save them to Google Drive.

- **`save_to_drive(self, id)`**: Downloads the images using their unique IDs and saves them as `.jpg` files.

## Notes

- Ensure you have the correct permissions and are logged in to Bing with the cookies provided.
- The script is designed to handle multiple users in parallel, enabling the generation of multiple prompts concurrently.

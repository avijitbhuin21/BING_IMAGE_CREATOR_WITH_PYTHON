# BING_IMAGE_CREATOR_WITH_PYTHON
programmatically using the bing image creator

Example Use:
import json
from Bing_Image_Generator import Image_Gen
data = json.load(open("templates\cookies.json")) <-- loading cookies from "cookies.json" file
image_generator = Image_Gen(all_cookies=data)
res=image_generator.Generate(prompt=prompt)
return res <-- it will return a list of four links containing the pictures.

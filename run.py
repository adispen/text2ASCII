from flask import Flask, request, redirect
import twilio.twiml
import urllib2
import requests
import sys
from PIL import Image
import numpy as np

app = Flask(__name__)

ascii_chars = [ '#', 'A', '@', '%', 'S', '+', '<', '*', ':', ',', '.']

def image_to_ascii(image):
    image_as_ascii = []
    all_pixels = list(image.getdata())
    for pixel_value in all_pixels:
        index = pixel_value / 25 # 0 - 10
        image_as_ascii.append(ascii_chars[index])
    return image_as_ascii   

def asciiConvert(imgName):
    img = Image.open(imgName)
    width, heigth = img.size
    new_width = 80 
    new_heigth = int((heigth * new_width) / width)
    new_image = img.resize((new_width, new_heigth))
    new_image = new_image.convert("L") # convert to grayscale
        
    # now that we have a grayscale image with some fixed width we have to convert every pixel
    # to the appropriate ascii character from "ascii_chars"
    img_as_ascii = image_to_ascii(new_image)
    img_as_ascii = ''.join(ch for ch in img_as_ascii)
    for c in range(0, len(img_as_ascii), new_width):
        print img_as_ascii[c:c+new_width]

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    print str(request.values)
    url = request.form['MediaUrl0']
    print url
    imgType = request.form['MediaContentType0']
    imgSave = url.rsplit('/',1)[1]
    r = requests.get(url, stream=True)
    with open(imgSave, "wb") as f:
        f.write(r.content)
    asciiConvert(imgSave)
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

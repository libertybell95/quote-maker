#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import time
from tqdm import tqdm

def maxCharSize(size, fontFile="Lato-Regular.ttf"):
    # Get the max pixel size of a character of a specific font and size.
    with open("quotes.txt", "r") as file:
        chars = set(list(file.read()))
    
    font = ImageFont.truetype(fontFile, size)

    heights = []
    widths = []
    for c in chars:
        w, h = font.getsize(c)
        heights.append(h)
        widths.append(w)

    return {
        "height": max(heights),
        "width": max(widths)
    }

def lineWidth(text, size=50, fontFile="Lato-Regular.ttf"):
    # Get string pixel width
    font = ImageFont.truetype(fontFile, size)
    w, h = font.getsize(text)
    return w

def multiline(text):
    # Calculate multiple lines, output as string with \n and spaces
    allowedWidth = 1920 - (50 * 2)
    # maxLetters = int(allowedWidth / maxCharSize(50)["width"]) # Max letters allowed per line
    maxLetters = 70

    text = text.replace("  ", " ").replace("\n", "")
    
    if len(text) <= maxLetters: # If quote can fit into one sentence.
        return {
            "text": text,
            "height": maxCharSize(50)["height"],
            "width": lineWidth(text)
        }
    else: # If quote cannot fit into one sentence.
        currentIdx = maxLetters - 1
        seperator = "\n   "
        lines = []
        while True:
            if currentIdx < len(text) and len(text) >= maxLetters:
                if text[currentIdx] == " ":
                    lines.append(text[:currentIdx] + seperator)
                    text = text[currentIdx:]
                    currentIdx = maxLetters - 1
                else:
                    currentIdx -= 1
                    continue
            elif len(text) <= maxLetters:
                lines.append(text)
                break
            else:
                break
    
        return {
            "text": "".join(lines),
            "height": maxCharSize(50)["height"] * len(lines),
            "width": max([lineWidth(i) for i in lines])
        }
                
def makeImage(text, textHeight, textWidth, outFile="test.png"):
    # Make an image
    image = Image.open("blank.png")
    draw = ImageDraw.Draw(image)
    imWidth, imHeight = image.size
    centerX, centerY = imWidth / 2, imHeight / 2

    font = ImageFont.truetype("Lato-Regular.ttf", 50)
    draw.text(
        (
            centerX - (textWidth / 2), # X Coord (Top left)
            centerY - (textHeight / 2) # Y Coord (Top left)
        ), 
        text, 
        font=font, 
        align="left"
        )
    image.save("images/{}".format(outFile))

def bulkProcess():
    # Process all quotes
    with open("quotes.txt", "r") as file:
        lines = [i.replace("\n", "") for i in file.readlines() if i != "" and i != "\n"].reverse()

    with tqdm(total=len(lines), unit="image", desc="Image Generation") as pbar:
        for idx, text in enumerate(lines):
            m = multiline(text)
            makeImage(text=m["text"], textHeight=m["height"], textWidth=m["width"], outFile="{}.png".format(idx))
            pbar.update(1)
            # print("{} of {} completed".format(idx+1, len(lines)))

def singleProcess(text):
    # Process single quote
    m = multiline(text)
    makeImage(text=m["text"], textHeight=m["height"], textWidth=m["width"])

if __name__ == "__main__":
    bulkProcess()

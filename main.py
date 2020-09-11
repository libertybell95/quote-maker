#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

class quote:
    def __init__(self):
        self.quoteFile = "quotes.txt" # Text file of quotes
        self.fontFile = "Lato-Regular.ttf" # Font .ttf file
        self.fontSize = 50 # Size of the font.
        self.maxLetters = 70 # Maximum amount of characters in one line.
        self.resolution = (1920, 1080) # Image size/resolution.
        self.maxSize = self.maxCharSize()

    def bulkProcess(self):
        # Process all quotes
        with open(self.quoteFile, "r") as file:
            lines = [i.replace("\n", "") for i in file.readlines() if i != "" and i != "\n"]
            lines.reverse()
        
        with tqdm(total=len(lines), unit="image", desc="Image Generation") as pbar:
            for idx, val in enumerate(lines):
                self.makeImage(val, idx)
                pbar.update(1)

    def singleProcess(self):
        # Process single quote
        self.makeImage(input("Quote: "))
    
    def maxCharSize(self) -> dict:
        # Get max possible pixel size of a single character.
        with open(self.quoteFile, "r") as file:
            chars = set(list(file.read()))

        font = ImageFont.truetype(self.fontFile, self.fontSize)
        heights, widths = [], []
        for c in chars:
            w, h = font.getsize(c)
            heights.append(h)
            widths.append(w)

        return {
            "height": max(heights),
            "width": max(widths)
        }
    
    def lineWidth(self, text: str) -> int:
        # Get string pixel width
        font = ImageFont.truetype(self.fontFile, self.fontSize)
        return font.getsize(text)[0]

    def multiline(self, text: str) -> dict:
        text = text.replace("  ", " ").replace("\n", "")

        if len(text) <= self.maxLetters: # If quote can fit into one sentence.
            return {
                "text": text,
                "height": self.maxCharSize()["height"],
                "width": self.lineWidth(text)
            }
        else: # If quote cannot fit into one sentence.
            currentIdx = self.maxLetters - 1
            seperator = "\n   "
            lines = []
            while True:
                if currentIdx < len(text) and len(text) >= self.maxLetters:
                    if text[currentIdx] == " ":
                        lines.append(text[:currentIdx] + seperator)
                        text = text[currentIdx:]
                        currentIdx = self.maxLetters - 1
                    else:
                        currentIdx -= 1
                        continue
                elif len(text) <= self.maxLetters:
                    lines.append(text)
                    break
                else:
                    break
        
            return {
                "text": "".join(lines),
                "height": self.maxCharSize()["height"] * len(lines),
                "width": max([self.lineWidth(i) for i in lines])
            }
    
    def makeImage(self, text: str, outFile: str="test"):
        # Make an image
        image = Image.new("RGB", self.resolution, color="black")
        draw = ImageDraw.Draw(image)
        centerX, centerY = self.resolution[0] / 2, self.resolution[1] / 2

        font = ImageFont.truetype(self.fontFile, self.fontSize)
        lines = self.multiline(text)
        draw.text(
            (
                centerX - (lines["width"] / 2), # X Coord (Top left)
                centerY - (lines["height"] / 2) # Y Coord (Top left)
            ), 
            lines["text"], 
            font=font,
            align="left"
            )

        image.save("images/{}.png".format(outFile))

if __name__ == "__main__":
    quote().bulkProcess()

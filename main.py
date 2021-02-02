#!/usr/bin/env python3

from typing import Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import re

class Profanity:
    @property
    def badWords(self) -> List[str]:
        with open("bad-words.txt", "r") as file:
            return map(lambda w:w.strip().lower(), file.readlines())

    def check(self, string: str) -> bool:
        string = string.lower()
        for word in self.badWords:
            if re.search(r'\b'+word+r'\b', string):
                return word
        return False

class ImageMaker:
    def __init__(self, quote: str, fontFile: str="Lato-Regular.ttf", fontSize: float=50, maxLineChars: int=70, resolution: Tuple[int]=(1920,1080)) -> None:
        self.quote = re.sub(" +", " ", quote).strip()
        self.fontFile = fontFile
        self.fontSize = fontSize
        self.font = ImageFont.truetype(self.fontFile, self.fontSize)
        self.maxLineChars = maxLineChars
        self.resolution = resolution

    def maxCharSize(self) -> Dict[int, int]:
        heights, widths = [], []
        for c in set(list(self.quote)):
            w, h = self.font.getsize(c)
            heights.append(h)
            widths.append(w)

        return {
            "height": max(heights),
            "width": max(widths)
        }

    def lineWidth(self, string: str) -> int:
        return self.font.getsize(string)[0]

    def multiline(self) -> dict:
        if len(self.quote) <= self.maxLineChars: # If quote can fit onto one line
            return {
                "text": self.quote,
                "height": self.maxCharSize()["height"],
                "width": self.lineWidth(self.quote)
            }
        else: # If quote cannot fit onto one line
            currentIdx = self.maxLineChars - 1
            seperator = "\n   "
            lines = []
            
            while True:
                if currentIdx < len(self.quote) and len(self.quote) >= self.maxLineChars:
                    if self.quote[currentIdx] == " ":
                        lines.append(self.quote[:currentIdx] + seperator)
                        self.quote = self.quote[currentIdx:]
                        currentIdx = self.maxLineChars - 1
                    else:
                        currentIdx -= 1
                        continue
                elif len(self.quote) <= self.maxLineChars:
                    lines.append(self.quote)
                    break
                else:
                    break
            
            return {
                "text": "".join(lines),
                "height": self.maxCharSize()["height"] * len(lines),
                "width": max([self.lineWidth(i) for i in lines])
            }

    def save(self, outFile="test"):
        image = Image.new("RGB", self.resolution, color="black")
        draw = ImageDraw.Draw(image)
        centerX, centerY = self.resolution[0] / 2, self.resolution[1] / 2

        lines = self.multiline()
        draw.text(
            (
                centerX - (lines["width"] / 2), # X-Coord (Top Left)
                centerY - (lines["height"] / 2) # Y-Coord (Top Left)
            ),
            lines["text"],
            font=self.font,
            align="left"
        )

        image.save("images/"+outFile+".png")

class Process:
    def __init__(self, censor=False) -> None:
        self.censor = censor

    def single(self):
        quote = input("Quote: ")
        if self.censor and Profanity().check(quote):
            print("Profanity found, aborting")
            return None

        ImageMaker(quote).save()    

    def bulk(self, quoteFile: str):
        with open(quoteFile, "r") as file:
            quotes = [i.strip() for i in file.readlines() if i.strip() != ""]
            quotes.reverse()

        with tqdm(total=len(quotes), unit="image", desc="Image Generation") as pbar:
            for idx, quote in enumerate(quotes):
                if self.censor and Profanity().check(quote):
                    print("Profanity found, skipping")
                    pbar.update(1)
                    continue
                ImageMaker(quote).save(str(idx))
                pbar.update(1)
    

if __name__ == "__main__":
    Process(censor=True).bulk("quotes.txt")

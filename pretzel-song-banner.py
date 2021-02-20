import json
from PIL import Image, ImageDraw, ImageFont
import time

#Variables Change if needed
PathToJSON = 'songinfo.json' #Path to the JSON File
PathToCover = 'cover.jpg'
updateTime = 5 #Interval between Updates (Default 5 Seconds)

includePretzelLogo = True #Inculed Pretzel Logo True/False (Default: True)

#Custom Logo
includeCustomLogo = True #Includes Custom Logo True/False (Default: False)
logoPath = "logo.png" #Path\to\logo.png
logoPosition = (890,-10)

#let it be
old_track = ''
returned = 0

#Function for getting JSON Data
def get_info():
    #Opens the Songinfo JSON File
    with open(PathToJSON) as f:
        global data
        data = json.load(f)
    #Extracts JSON Data and gets the Cover File

#Function to Genarate the Banner
def gen_banner(track, artist):
    #get Cover
    #Creates the Background
    img = Image.new('RGB', (1000, 300), color = (23, 36, 45))
    #Pastes the Cover Art
    cover = Image.open(PathToCover)
    img.paste(cover, (0,0))
    d = ImageDraw.Draw(img)
    #Adds Pretzel Logo if True
    if includePretzelLogo == True:
        pl = Image.open("pretzellogo.png")
        img.paste(pl, (770,230), pl.convert('RGBA'))
    #Adds Custom Logo if True
    if includeCustomLogo == True:
        logo = Image.open(logoPath)
        img.paste(logo, logoPosition, logo.convert('RGBA'))
    #Writes down the Track and Artists
    tfont = ImageFont.truetype("arial.ttf", 80)
    afont = ImageFont.truetype("arial.ttf", 40)
    d.text((310,50), track, font=tfont, fill=(255, 255, 240))
    d.text((310,140), artist, font=afont, fill=(190, 190, 190))
    #save
    img.save('banner.png')

def paused():
    img = Image.new('RGBA', (1000, 300), color = (0, 0, 0, 0))
    img.save('banner.png')

def update(forced):
    global old_track
    track = data["track"]["title"]
    if forced == 1:
        old_track = track
        get_info()
        artist = data["track"]["artistsString"]
        gen_banner(track, artist)
        time.sleep(updateTime)
    if old_track == track:
        time.sleep(updateTime)
        return
    else:
        old_track = track
        get_info()
        artist = data["track"]["artistsString"]
        gen_banner(track, artist)
        time.sleep(updateTime)


while True:
    get_info()
    if data["player"]["playing"] == False:
        paused()
        returned = 1
        time.sleep(updateTime)
    elif returned == 1:
        update(1)
        returned = 0
    elif data["player"]["playing"] == True:
        update(0)

from colorthief import ColorThief
import requests
import re
import shutil
import webbrowser

def GetAlbumColor(albumName):
    albumImage = GetAlbum(albumName)
    if(albumImage != False):
        color_theif = ColorThief(albumImage)
        dominant_color = color_theif.get_palette(color_count=6,quality=3)
        webbrowser.open_new_tab('http://www.wolframalpha.com/input/?i=RGB+' + str(dominant_color[0]))     #get rid of this line to get rid of launching wolframalpha
        return dominant_color
    else:
        print("No Album Found")
        return False

def GetAlbum(query):
    query = 'http://www.last.fm/search?q=' + query.replace(' ', '+')
    content = requests.get(query).content.decode('utf-8')
    content = content.split('Albums', 1)[-1]

    foundAlbum = False
    if "No albums found" not in content:
        while(True):
            imageURL = re.search('src="https://lastfm-img2.akamaized.net/i/u/300x300/(.*)"', content)
            if(imageURL):
                imageURL = 'https://lastfm-img2.akamaized.net/i/u/300x300/' + imageURL.group(1);
                fileType = imageURL[-3:]

                response = requests.get(imageURL, stream=True)
                fileName = 'img.'+fileType
                
                with open(fileName, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                if(not (fileType == 'png' and (open(fileName,"rb").read() == open("defaultAlbum.png","rb").read()))):
                    webbrowser.open_new_tab(imageURL)               #get rid of this line to get rid of launching the image
                    foundAlbum = True
                    break
                else:
                    content = content.split(imageURL, 1)[-1]
            else:
                break
        
    else:
        print("No albums found")
    if(foundAlbum):
        return 'img.'+fileType;
    return False
    
# Example use
print(GetAlbumColor("8 Million Stories"))

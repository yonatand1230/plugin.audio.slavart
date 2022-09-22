import sys
import xbmcgui
import xbmcplugin
import urllib
import urllib.parse 
import json
from urllib.request import urlopen
import os
import time
import requests
import sys

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urllib.parse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'songs')

def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)
mode = args.get('mode', None)

def getResults(entry, type):
    url = "https://slavart.gamesdrive.net/api/search?q=" + entry
    response = urlopen(url)
    global json_data
    json_data = json.loads(response.read())

'''
## GET RESULTS FROM REMOTE JSON INTO DICT 'SimpleData' ##
def getResults(entry, type):
    #global simpleData
    #simpleData = {}
    global url
    url = "https://slavart.gamesdrive.net/api/search?q=" + entry
    response = urlopen(url)
    global json_data
    json_data = 
    
    if type=='track':
        for i in range(0,10):
            result_num = 'r' + str(i+1)
            newId = json_data.get('tracks').get('items')[i].get('id')
            newId = str(newId)
            newArtist = json_data.get('tracks').get('items')[i].get('performer').get('name')
            newTitle = json_data.get('tracks').get('items')[i].get('title')
            newImage = json_data.get('tracks').get('items')[i].get('album').get('image').get('large')
            newAlbum = json_data.get('tracks').get('items')[i].get('album').get('title')
            newDuration = json_data.get('tracks').get('items')[i].get('duration')
            
            fullName = newArtist + ' - ' + newTitle
            simpleData.update({result_num:{'id':newId, 'title':newTitle, 'artist':newArtist, 'albm':newAlbum,'img':newImage, 'full':fullName, 'dur':newDuration}})
    elif type=='album':
        for i in range(0,10):
            result_num = 'r' + str(i+1)
            newId = json_data.get('albums').get('items')[i].get('id')
            newId = str(newId)
            newArtist = json_data.get('albums').get('items')[i].get('artists')[0].get('name')
            newTitle = json_data.get('albums').get('items')[i].get('title')
            newImage = json_data.get('albums').get('items')[i].get('image').get('small')
            
            bitDepth = json_data.get('albums').get('items')[i].get('maximum_bit_depth')
            sampleRate = json_data.get('albums').get('items')[i].get('maximum_sampling_rate')
            res=''
            if json_data.get('albums').get('items')[i].get('hires') == True:
                res=' [Hi-Res]'
            elif bitDepth==16 and sampleRate==44.1:
                res=' [CD Quality]'
            
            newAlbum = str(bitDepth) + '-bit \\ ' + str(sampleRate) + 'kHz' + res
            
            simpleData.update({result_num:{'id':newId, 'title':newTitle, 'artist':newArtist, 'albm':newAlbum,'img':newImage}})
'''


dialog = xbmcgui.Dialog()
inpt = dialog.input('Enter a Track Name:', type=xbmcgui.INPUT_ALPHANUM)
inpt = inpt.replace(' ', '%20')
getResults(inpt, 'track')


# SHOW RESULTS
for i in range(1,25):
    num = 'r' + str(i)
    trkVr = json_data.get('tracks').get('items')[i].get('version')
    trkVrTxt = ''
    
    if not trkVr==None:
        trkVrTxt = ' [' + trkVr + ']'
    fullName = json_data.get('tracks').get('items')[i].get('performer').get('name') + ' - ' + json_data.get('tracks').get('items')[i].get('title') + trkVrTxt
    li = xbmcgui.ListItem(fullName)
    li.setArt({'icon':json_data.get('tracks').get('items')[i].get('album').get('image').get('large')})
    
    
    trkYear = int(json_data.get('tracks').get('items')[i].get('album').get('release_date_original')[:4])
    trkAlbm = json_data.get('tracks').get('items')[i].get('album').get('title')
    trkDur = json_data.get('tracks').get('items')[i].get('duration')
    trkGenre = json_data.get('tracks').get('items')[i].get('album').get('genre').get('name')
    trkNum = json_data.get('tracks').get('items')[i].get('track_number')
    trkArtst = json_data.get('tracks').get('items')[i].get('performer').get('name')
    trkTtl = json_data.get('tracks').get('items')[i].get('title')
    
    
    li.setInfo('music', {'duration':trkDur, 'genre':trkGenre, 'tracknumber':trkNum, 'year':trkYear, 'artist':trkArtst, 'title':trkTtl, 'mediatype':'music', 'album':trkAlbm})
    url = 'https://slavart-api.gamesdrive.net/api/download/track?id=' + str(json_data.get('tracks').get('items')[i].get('id'))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    trkVr = ''
    trkVrTxt = ''



xbmcplugin.endOfDirectory(addon_handle)



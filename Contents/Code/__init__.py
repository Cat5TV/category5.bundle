# Version 1.7

import sys, os, urlparse, urllib, urllib2, cookielib, re, json, time

TITLE = 'Category5 TV Network'
PREFIX = '/video/category5'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0'

#####################################################################################################################################

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-default.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.jpg')

    Plugin.AddPrefixHandler("/video/category5", MainMenu, L('Category5.TV'), DirectoryObject.thumb, DirectoryObject.art)
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'
    HTTP.CacheTime = CACHE_1HOUR

    Log("Category5 plugin started!!!")

#####################################################################################################################################

@handler(PREFIX, TITLE)
def MainMenu():
    oc = ObjectContainer()

    oc.add(DirectoryObject(key=Callback(ShowLive, title="Category5 Live Stream", url='http://servers.minetest.tv:8081/live/cat5tv/playlist.m3u8'), summary="Watch the live stream every Wednesday night at 7pm (Toronto time). For local showtimes, visit category5.tv/timezones", thumb='http://cdn3.taliferguson.com/img/live/default/512x512.jpg'))
    oc.add(DirectoryObject(key=Callback(ShowRSS, title="Category5 Technology TV", url='http://rss.cat5.tv/plex/tech-hd.rss'), summary="Weekly live digital TV show with Robbie Ferguson focused on topics of interest to tech minds. Ask your questions and get live answers. Recipient of 2014 and 2017 Top 100 Tech Podcasters award.", thumb='http://cdn3.taliferguson.com/img/tech/default/512x512.jpg'))
    oc.add(DirectoryObject(key=Callback(ShowRSS, title="Category5.TV Newsroom", url='http://rss.cat5.tv/plex/newsroom-hd.rss'), summary="A weekly tech-centric news broadcast with a Linux bias (Part of Category5 Technology TV).", thumb='http://cdn3.taliferguson.com/img/newsroom/default/512x512.jpg?1.0'))
    oc.add(DirectoryObject(key=Callback(ShowRSS, title="New Every Day", url='http://rss.cat5.tv/plex/ned-hd.rss'), summary="Join Jenn Wagar and Carrie Webb as they sit down for a heart-to-heart discussion each week, addressing many of the issues Christians face in their day to day lives, and building your faith and focus through relevant conversation.", thumb='http://cdn3.taliferguson.com/img/ned/default/512x512.jpg'))
    oc.add(DirectoryObject(key=Callback(ShowRSS, title="The Pixel Shadow", url='http://rss.cat5.tv/plex/tps-hd.rss'), summary="Minetest (The Free Minecraft Alternative) runs on Linux, Mac and Windows, and we'll show you how to play.", thumb='http://cdn3.taliferguson.com/img/tps/default/512x512.jpg'))
    oc.add(DirectoryObject(key=Callback(ShowRSS, title="Immersive Nature Sounds", url='http://rss.cat5.tv/plex/nature-hd.rss'), summary="Relax, study or work with peaceful natural sounds recorded in 360 VR.", thumb='http://cdn3.taliferguson.com/img/nature/default/512x512.jpg'))
    oc.add(DirectoryObject(key=Callback(ShowRSS, title="Category5 Technology TV - Clips", url='http://rss.cat5.tv/plex/clips_tech-hd.rss'), summary="Clips from Category5 Technology TV.", thumb='http://cdn3.taliferguson.com/img/clips_tech/default/512x512.jpg'))
    return oc

#####################################################################################################################################

@route(PREFIX + '/showlive')
def ShowLive(title, url):

    oc = ObjectContainer()
    oc.add(CreateVideoClipObject(
        url = url,
        title = title,
        thumb = 'http://cdn3.taliferguson.com/img/tech/default/thumb.jpg',
        summary = "Watch the live stream every Wednesday night at 7pm (Toronto time). For local showtimes, visit category5.tv/timezones"
     ))
    return oc

#####################################################################################################################################

@route(PREFIX + '/showrss')

def ShowRSS(title, url):

    # requests the sourcecode for a webpage
    sourceCode = getURL(url)

    # removes all new lines or character returns from the source code
    sourceCode1 = sourceCode.replace('\n', ' ').replace('\r', '')

    # searches the sourcecode and gets anything between the cat5tv:number tags and places it into the variable numberrss
    numberrss = re.findall(r'<cat5tv:number>(.*?)</cat5tv:number>', sourceCode)

    # searches the sourcecode and gets anything between the cat5tv:title tags and places it into the variable titlerss
    titlerss = re.findall(r'<cat5tv:title>(.*?)</cat5tv:title>', sourceCode)

    # searches the sourcecode and gets anything between the cat5tv:year tags and places it into the variable yearrss
    yearrss = re.findall(r'<cat5tv:year>(.*?)</cat5tv:year>', sourceCode)

    # searches the sourcecode and gets anything between the cat5tv:genre tags and places it into the variable genrerss
    genrerss = re.findall(r'<cat5tv:genre>(.*?)</cat5tv:genre>', sourceCode)

    # searches the sourcecode and gets anything between the cat5tv:description tags and places it into the variable descriptionrss
    descriptionrss = re.findall(r'<cat5tv:description>(.*?)</cat5tv:description>', sourceCode1)

    # searches the sourcecode and gets anything between the cat5tv:thumbnail tags and places it into the variable thumbnailrss
    thumbnailrss = re.findall(r'<cat5tv:thumbnail>(.*?)</cat5tv:thumbnail>', sourceCode)

    # searches the sourcecode and gets anything between the media:credit role="director" tags and places it into the variable directorrss
    directorrss = re.findall(r'<media:credit role="director">(.*?)</media:credit>', sourceCode)

    # searches the sourcecode and gets anything between the author tags and places it into the variable writerrss
    writerrss = re.findall(r'<author>(.*?)</author>', sourceCode)

    # searches the sourcecode and gets anything between the link tags and places it into the variable linksrss (m4v)
    linksrss = re.findall(r'<link>(.*?).m4v</link>', sourceCode)

    # checks to make sure linkrss has content for m4v if not check for mp3
    if len(linksrss) <= 0:

        # searches the sourcecode and gets anything between the link tags and places it into the variable linksrss (mp3)
        linksrss = re.findall(r'<link>(.*?).mp3</link>', sourceCode)

    oc = ObjectContainer()

    # loops through all data found from numberrss, titlerss, thumbnailrss and adds information to list item

    for rssnumber, rsstitle, rssyear, rssgenre, rssdescription, rssdirector, rssthumbnail, rsslinks, rsswriter in zip(numberrss, titlerss, yearrss, genrerss, descriptionrss, directorrss, thumbnailrss, linksrss, writerrss):

        title = rssnumber + ' - ' + rsstitle

        oc.add(CreateVideoClipObject(
                                     url = rsslinks,
                                     title = title,
                                     thumb = rssthumbnail,
                                     summary = rssdescription
                                     ))

    return oc

#####################################################################################################################################

@route(PREFIX + '/getURL')
def getURL(url):

    # sets the header for any website.  This will instuct any webserver the request is set to mozilla
    headercode = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    # opens up a link to the webserver and requests the webpage to see if valid
    openurl = urllib2.Request(url, headers=headercode)

    # opens a connection  to the webpage
    response = urllib2.urlopen(openurl)

    # reads all the sourcecode of the webpage
    source = response.read()

    # returns the source code
    return source


#####################################################################################################################################

# This is a function to pull the thumb from a the head of a page
@route(PREFIX + '/getthumb')
def GetThumb(url):

    page = HTML.ElementFromURL(url)
    try:
        thumb = page.xpath("//head//meta[@property='og:image']//@content")[0]
        if not thumb.startswith('http://'):
            thumb = http + thumb
    except:
        thumb = R('icon-default.png')

    return thumb

#####################################################################################################################################
@route(PREFIX + '/createvideoclipobject')
def CreateVideoClipObject(url, title, thumb, summary, include_container=False):

    videoclip_obj = VideoClipObject(
                                    key = Callback(CreateVideoClipObject, url=url, title=title, thumb=thumb, summary=summary, include_container=True),
                                    rating_key = url,
                                    title = title,
                                    thumb = thumb,
                                    summary = summary,
                                    items = [
                                             MediaObject(
                                                         parts = [
                                                                  PartObject(key=url)
                                                                  ],
                                                         container = Container.MP4,
                                                         video_codec = VideoCodec.H264,
                                                         audio_codec = AudioCodec.AAC,
                                                         audio_channels = 2,
                                                         optimized_for_streaming = True
                                                         )
                                             ]
                                    )
    if include_container:
        return ObjectContainer(objects=[videoclip_obj])
    else:
        return videoclip_obj

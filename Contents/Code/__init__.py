import sys, os, urlparse, urllib, urllib2, cookielib, re, json, time


TITLE = 'Category5.TV'
PREFIX = '/video/category5'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0'

#####################################################################################################

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-default.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.jpg')
    
    Plugin.AddPrefixHandler("/video/category5", MainMenu, L('Category5.TV'), DirectoryObject.thumb, DirectoryObject.art)
    Plugin.AddViewGroup('List', viewMode='Details', mediaType='items')
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
    Log("Category5 plugin started!!!")

#####################################################################################################

@handler(PREFIX, TITLE)
def MainMenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(cat5tech), title="Technology", thumb=R('art-default.jpg')))
    return oc

#####################################################################################################

@route(PREFIX + '/cat5tech')
def cat5tech():
    oc = ObjectContainer()

    video_title = "Raspberry Pi Music Server - Part 1 - Category5 Technology TV - Episode 414"
    link = "http://v.cat5.tv/a/h73as8g/v/e/i/1442/q/hd/CAT5TV-414-Raspberry-Pi-Music-Server-Part-1-HD.m4v"
    image = "http://cdn3.taliferguson.com/img/tech/414/200.jpg"
    summarys = "We're building a music server that fits in your pocket. Robbie and Sasha kick off our 3-part Raspberry Pi Music Server series with a Pi 2 kit that gets us started with the build."
    
    oc.add(VideoObject(
                       url = link,
                       title = video_title,
                       thumb = image,
                       summary = summarys,
                       ))
    video_title = "Google Analytics Fundamentals - Part 1 - Category5 Technology TV - Episode 413"
    link = "http://v.cat5.tv/a/h73as8g/v/e/i/1441/q/hd/CAT5TV-413-Google-Analytics-Fundamentals-Part-1-HD.m4v"
    image = "http://cdn3.taliferguson.com/img/tech/412/200.jpg"
    summarys = "Robbie and Erika introduce our series on Google Analytics, and how to use it to track web site visitors and generate helpful reports. This data can be used to show you where you're going wrong (or right) with your web site, and help you focus who your web site reaches and cater to your vistors better."
                       
    oc.add(VideoObject(
                       url = link,
                       title = video_title,
                       thumb = image,
                       summary = summarys,
                       ))
    return oc

#####################################################################################################

@route(PREFIX + '/videoobject')
def VideoObject(url, title, thumb, summary, include_container=False):
    
    videoclip_obj = VideoClipObject(
      key = Callback(VideoObject, url=url, title=title, thumb=thumb, summary=summary, include_container=True),
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

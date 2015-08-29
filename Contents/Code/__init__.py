TITLE = 'Category 5'
PREFIX = '/video/category5'

def Start():
    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R('art-default.jpg')
    DirectoryObject.thumb = R('icon-default.png')
    DirectoryObject.art = R('art-default.jpg')
    VideoClipObject.art = R('art-default.jpg')

@handler(PREFIX, TITLE)
def MainMenu():
    return 
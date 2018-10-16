# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem, Dialog
from xbmcplugin import addDirectoryItem, endOfDirectory

import urllib2
import urllib

import re

ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()
dialog = Dialog()

def Post(url,params):
    _params = urllib.urlencode(params)
    req = urllib2.Request(url,_params)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req).read()

def Get(url):
    # print(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    return urllib2.urlopen(req).read()

@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_search_input), ListItem("Search"), True)
    p = Get('http://www.1993s.top')
    it = re.finditer(r'<a class=\"stui-vodlist__thumb lazyload\" href=\"(.*?)\" title=\"(.*?)\" data-original=\"(.*?)\">',p)
    for match in it:
        id = re.search(r'(\d+)',match.group(1)).group()
        addDirectoryItem(plugin.handle, plugin.url_for(show_detail, id=id, img=match.group(3)), ListItem(match.group(2),thumbnailImage=match.group(3)), True)

    endOfDirectory(plugin.handle)

@plugin.route('/search_input')
def show_search_input():
    s = dialog.input('Search')
    # print s
    p = Post('http://www.1993s.top/index.php?s=vod-search',{ 'wd': s })
    # print p
    it = re.finditer( r'<a class=\"v-thumb stui-vodlist__thumb lazyload\" href=\"(.*?)\" title=\"(.*?)\" data-original=\"(.*?)\">', p)

    for match in it:
        id = re.search(r'\d+',match.group(1)).group()
        print match.group(2)
        # print id
        addDirectoryItem(plugin.handle, plugin.url_for(
            show_detail, id=id, img=match.group(3)), ListItem(match.group(2),thumbnailImage=match.group(3)), True)

    endOfDirectory(plugin.handle)

# @plugin.route('/category/<category_id>')
# def show_category(category_id):
#     addDirectoryItem(
#         plugin.handle, "", ListItem("Hello category %s!" % category_id))
#     endOfDirectory(plugin.handle)

@plugin.route('/Detail')
def show_detail():
    img = plugin.args['img'][0]
    id = plugin.args['id'][0]
    # print id
    # print img
    p = Get('http://www.1993s.top/detail/' + id + '.html')
    it = re.finditer(r'<a title=\"(.*?)\" href=\"(.*?)\">(?:.*?)</a>',p)

    plot = ''
    plotObj = re.search(r'<span class=\"detail-content\" style=\"display: none;\">(.*)',p)
    if plotObj:
        plot = plotObj.group(1)

    for match in it:
        vid = re.search(r'(\d+-\d+-\d+)',match.group(2)).group()
        li = ListItem(match.group(1),thumbnailImage=img)
        li.setInfo('video',{
            'plot': plot
        })
        addDirectoryItem(plugin.handle, plugin.url_for(play_Video, video=vid, img=img, plot=plot), li, True)

    endOfDirectory(plugin.handle)

@plugin.route('/video')
def play_Video():
    img = plugin.args['img'][0]
    video_url = plugin.args['video'][0]
    plot = plugin.args['plot'][0]
    # print '=======================>'
    # print video_url
    p = Get('http://www.1993s.top/video/' + video_url + '.html')
    match = re.search(r'\"url\":\"(.*?mp4)\"',p)
    print match.group(1).replace('\/','/')
    title = re.search(r'<h4 class=\"title\"><a href=\".*?\">(.*?)</a></h4>',p).group(1)
    li = ListItem(title + ' ' + video_url,thumbnailImage=img)

    # plot = ''
    # plotObj = re.search(r'<span class=\"left text-muted\">简介：</span><p>(.*?)</p>',p)
    # if plotObj:
    #     plot = plotObj.group(1)

    # print '=======================>'
    # print plot

    li.setInfo("video",{
    #     'director': jsonArr['list']['anime']['author'],
        'title': title,
    #     'originaltitle': jsonArr['list']['anime']['name_jpn'],
        'plot': plot
    #     'sorttitle': jsonEpisodes['title'],
    #     'status': jsonArr['list']['anime']['is_ended']
    })
    video_url = match.group(1).replace('\/','/')
    addDirectoryItem(plugin.handle, video_url, li)
    endOfDirectory(plugin.handle)

def run():
    plugin.run()

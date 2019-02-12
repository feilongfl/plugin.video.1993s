# -*- coding: utf-8 -*-

import routing
import logging
import xbmcaddon
from resources.lib import kodiutils
from resources.lib import kodilogging
import xbmc
from xbmcgui import ListItem, Dialog, DialogProgress
from xbmcplugin import addDirectoryItem, endOfDirectory

import urllib2
import urllib

import re
from resources.lib import decode


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()
dialog = Dialog()

# print(decode.var['decode']("333131666032373235613366603036693465646330356166616831333665693D3F54616629343369333564346237363364366332313366336160383632603333626736303D3F5B6166213533333539333033363435313D3033363435313F54716F34307D6E24686F23333562663361636636343460303336326262603533613533656938373939373F22616F22663F22303F2F656469667F2D6F636E276E69687F6168636E23716E616E616E21337F2F2A307474786"))

def Post(url,params,referer=None):
    _params = urllib.urlencode(params)
    req = urllib2.Request(url,_params)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    if referer != None:
        req.add_header('Referer', referer)

    return urllib2.urlopen(req).read()

def Get(url, referer=None):
    # print(url)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    if referer != None:
        req.add_header('Referer', referer)

    return urllib2.urlopen(req).read()

def playUrl(video_url,img,plot):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    li = ListItem(path=video_url,thumbnailImage=img)
    li.setInfo( type="video", infoLabels={ "Path" : video_url, "plot": plot,} )
    playlist.add(url=video_url, listitem=li)
    xbmc.Player().play(playlist)


@plugin.route('/')
def index():
    addDirectoryItem(plugin.handle, plugin.url_for(
        show_search_input), ListItem("Search"), True)
    p = Get('http://www.zxzjs.com')
    it = re.finditer(r'<a class=\"stui-vodlist__thumb lazyload\" href=\"(.*?)\" title=\"(.*?)\" data-original=\"(.*?)\">',p)
    for match in it:
        id = re.search(r'(\d+)',match.group(1)).group()
        addDirectoryItem(plugin.handle, plugin.url_for(show_detail, id=id, img=match.group(3)), ListItem(match.group(2),thumbnailImage=match.group(3)), True)

    endOfDirectory(plugin.handle)

@plugin.route('/search_input')
def show_search_input():
    s = dialog.input('Search')
    # print s
    # p = Post('http://www.zxzjs.com/index.php?s=vod-search',{ 'wd': s })
    p = Get('https://www.zxzjs.com/vodsearch/-------------.html?wd=%s' % s)
    # print p
    # it = re.finditer( r'<a class=\"v-thumb stui-vodlist__thumb lazyload\" href=\"(.*?)\" title=\"(.*?)\" data-original=\"(.*?)\">', p)
    it = re.finditer(r'<a class="stui-vodlist__thumb lazyload" href="(.*?)" title="(.*?)" data-original="(.*?)">', p)

    for match in it:
        id = re.search(r'\d+',match.group(1)).group()
        print match.group(2)
        # print id
        addDirectoryItem(plugin.handle, plugin.url_for(
            show_detail, id=id, img=match.group(3)), ListItem(match.group(2),thumbnailImage=match.group(3)), True)

    endOfDirectory(plugin.handle)

# @plugin.route('/category/<category_id>')
# def show_category(decode.decode(code)category_id):
#     addDirectoryItem(
#         plugin.handle, "", ListItem("Hello category %s!" % category_id))
#     endOfDirectory(plugin.handle)

@plugin.route('/Detail')
def show_detail():
    img = plugin.args['img'][0]
    id = plugin.args['id'][0]
    # print id
    # print img
    p = Get('http://www.zxzjs.com/detail/' + id + '.html')
    it = re.finditer(r'<a href="/video/(.*?)\.html">(.*?)</a>',p)

    plot = ''
    plotObj = re.search(r'<span class="detail-content" style="display: none;">([\s\S]+?)</span>',p)
    if plotObj:
        plot = plotObj.group(1)

    for match in it:
        vid = match.group(1)
        li = ListItem(match.group(2),thumbnailImage=img)
        li.setInfo('video',{
            'plot': plot
        })
        if match.group(2) != "立即播放":
            addDirectoryItem(plugin.handle, plugin.url_for(play_Video, video=vid, img=img, plot=plot), li, True)

    endOfDirectory(plugin.handle)

@plugin.route('/video')
def play_Video():
    progress = DialogProgress()
    progress.create('Loading')
    progress.update(10, "", 'Loading Video Info', "")
    img = plugin.args['img'][0]
    video_url = plugin.args['video'][0]
    plot = plugin.args['plot'][0]
    # print '=======================>'
    progress.update(30, "", 'Loading Web Files', "")
    # print video_url
    p = Get('http://www.zxzjs.com/video/' + video_url + '.html')
    # match = re.search(r'\"url\":\"(.*?mp4)\"',p)
    # match = re.search(r'cms_player\s*=\s*{"url":"(.*?)"',p)
    match = re.search(r'url":"(https.*?)"',p)

    #print match.group(1).replace('\/','/')
    #title = re.search(r'<h4 class=\"title\"><a href=\".*?\">(.*?)</a></h4>',p).group(1)
    title = "video"
    # li = ListItem(title + ' ' + video_url,thumbnailImage=img)

    # plot = ''
    # plotObj = re.search(r'<span class=\"left text-muted\">简介：</span><p>(.*?)</p>',p)
    # if plotObj:
    #     plot = plotObj.group(1)

    # print '=======================>'
    # print plot

    # li.setInfo("video",{
    # #     'director': jsonArr['list']['anime']['author'],
    #     'title': title,
    # #     'originaltitle': jsonArr['list']['anime']['name_jpn'],
    #     'plot': plot
    # #     'sorttitle': jsonEpisodes['title'],
    # #     'status': jsonArr['list']['anime']['is_ended']
    # })
    video_url = match.group(1).replace("\\","")
    progress.update(60, "", "Analyse Video Url", "")

    print("0",video_url,'http://www.zxzjs.com/video/' + plugin.args['video'][0] + '.html')
    p = Get(video_url, referer='http://www.zxzjs.com/video/' + plugin.args['video'][0] + '.html')
    video_url = re.search(r"'(.*?)',", p).group(1)

    progress.update(90, "", "Decode Video Url", "")

    print("1",video_url)
    # video_url = str(decode.var['decode'](video_url)).replace("'","")
    video_url = decode.decode(video_url)
    print("2",video_url)


    #dialog.ok(video_url,video_url)
    progress.update(100, "", "", "")
    # addDirectoryItem(plugin.handle, video_url, li)
    progress.close()

    playUrl(video_url,img,plot)
    # endOfDirectory(plugin.handle)

def run():
    plugin.run()

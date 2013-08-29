import json
import re
import urllib2
from pyquery import PyQuery as pq

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

song_query = 'http://music.baidu.com/data/music/fmlink?songIds={}&type={}&rate={}'
pattern = re.compile(r'(http://)?music.baidu.com/song/(?P<song_id>\d*)')


def home(request):
    return render_to_response('index.html')


def song(request, song_id):
    song_dict = {
        'mp3_128': song_query.format(song_id, 'mp3', '128'),
        'mp3_192': song_query.format(song_id, 'mp3', '192'),
        'mp3_320': song_query.format(song_id, 'mp3', '320'),
        'flac': song_query.format(song_id, 'flac', '1411')
    }
    for key, value in song_dict.items():
        try:
            song_info = json.loads(urllib2.urlopen(value).read())['data']['songList'][0]
            if 'song_name' not in song_dict:
                song_dict['song_name'] = song_info['songName'].encode('utf8')
                song_dict['artist_name'] = song_info['artistName'].encode('utf8')
                song_dict['lrc_link'] = 'http://music.baidu.com' + song_info['lrcLink']
            song_dict[key] = {
                'size': '{:.1f}'.format(song_info['size'] / 1024.0**2),
                'rate': song_info['rate'],
                'link': song_info['songLink']
            }
        except:
            song_dict[key] = None
    return render_to_response('song.html', song_dict)


def search(request):
    if 'input_content' not in request.POST:
        return HttpResponseRedirect('/')

    input_content = request.POST['input_content']
    song_link_match = pattern.match(input_content)
    if song_link_match:
        song_id = song_link_match.group('song_id')
        return HttpResponseRedirect('/song/' + song_id)
    elif input_content.isdigit():
        return HttpResponseRedirect('/song/' + input_content)

    else:
        url = 'http://music.baidu.com/search?key=' + input_content.replace(' ', '+').encode('utf-8')
        page = urllib2.urlopen(url).read()
        d = pq(page.decode('utf-8'))
        song_list = d('li.song-item-hook')
        result = []

        for song in song_list:
            song = pq(song)
            song_info = json.loads(song.attr('data-songitem'))['songItem']
            song_dict = {}
            if not song('span.icon-thirdparty'):
                song_dict['link'] = '/song/' + str(song_info['sid'])
                song_dict['song_name'] = song_info['sname']
                song_dict['artist_name'] = song_info['author']
                song_dict['album_name'] = song('span.album-title > a').html()
                result.append(song_dict)
        return render_to_response('search.html', {'result': result})

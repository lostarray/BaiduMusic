import json
import re
import urllib2

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

song_query = 'http://music.baidu.com/data/music/fmlink?songIds={}&type={}&rate={}'
pattern = re.compile(r'(http://)?music.baidu.com/song/(?P<song_id>\d*)')


def home(request):
    if 'song_link' in request.POST:
        song_link = request.POST['song_link']
        song_link_match = pattern.match(song_link)
        if song_link_match:
            song_id = song_link_match.group('song_id')
            return HttpResponseRedirect('song/' + song_id)
        else:
            # Wrong input
            pass
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
            song_dict[key] = {
                'size': '{:.1f}'.format(song_info['size'] / 1024.0**2),
                'rate': song_info['rate'],
                'link': song_info['songLink']
            }
        except:
            song_dict[key] = None
    return render_to_response('down_song.html', song_dict)

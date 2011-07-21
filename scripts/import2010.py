# -*- coding:utf-8 -*-
from datetime import datetime
import feedparser
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from videos.models import Video, Tag, Url

def main():
    parsed = feedparser.parse(file('mostravideolivre.atom').read())
    for i in parsed.entries:
        mp4_url = i.content[0].src
        ogg_url = mp4_url.replace('.mp4', '.ogg')
        ogg_url = ogg_url.replace('.MP4', '.ogg')
        thumb = ogg_url + '.png'

        video = Video()
        video.title = i.title
        video.creation_date = datetime.now()
        video.summary = i.get('summary', '')
        video.author = i.author
        video.license_name = \
            'Creative Commons - Atribuição - Partilha nos Mesmos ' + \
            'Termos 3.0 Não Adaptada'
        video.license_link = 'http://creativecommons.org/licenses/by-sa/3.0/'
        video.thumb_url = thumb
        video.save()

        tag = Tag.objects.get_or_create(name='mvl2010')[0]
        tag.save()
        video.tags.add(tag.id)

        url = Url()
        url.url = mp4_url
        url.content_type = 'video/mp4; codecs="avc1.42E01E, mp4a.40.2"'
        url.video = video
        url.save()

        url = Url()
        url.url = ogg_url
        url.content_type = 'video/ogg; codecs="theora, vorbis"'
        url.video = video
        url.save()

if __name__ == '__main__':
    main()

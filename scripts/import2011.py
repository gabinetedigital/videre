# -*- coding:utf-8 -*-
from datetime import datetime
import csv
import os
import re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from videos.models import Video, Tag, Url

BASE_URL = 'http://mostra.videolivre.org.br/files/fisl_2011'
url_finder = re.compile(r'https?://[-a-zA-Z0-9+&@#/%?=~_|!:,.;]*[-a-zA-Z0-9+&@#/%=~_|]')


def findvideo(desc):
    urls = []
    for url in url_finder.findall(desc):
        if 'youtube' in url:
            fname = url.split('?')[1].split('=')[1]
            urls.append('%s/%s.ogv' % (BASE_URL, fname))

        elif 'vimeo' in url:
            fname = url.split('/')[-1]
            urls.append('%s/%s.ogv' % (BASE_URL, fname))
        else:
            urls.append(url)
    return urls[0]

def main():
    for index, line in enumerate(csv.reader(file('mostravideolivre.csv'))):

        # I don't need the column names :)
        if index == 0:
            continue

        # No title
        if not line[0].strip():
            continue

        video = Video()
        video.title = line[0]
        video.creation_date = datetime.now()
        video.summary = line[5]
        video.author = line[1]
        video.license_name = \
            'Creative Commons - Atribuição - Partilha nos Mesmos ' + \
            'Termos 3.0 Não Adaptada'
        video.license_link = 'http://creativecommons.org/licenses/by-sa/3.0/'
        video.thumb_url = findvideo(line[7]).replace('ogv', 'png')
        video.save()

        tag = Tag.objects.get_or_create(name='mvl2011')[0]
        tag.save()
        video.tags.add(tag.id)
        for tag_name in line[4].split(','):
            tag = Tag.objects.get_or_create(name=tag_name.strip())[0]
            tag.save()
            video.tags.add(tag.id)

        url = Url()
        url.url = findvideo(line[7])
        url.content_type = 'video/ogg; codecs="theora, vorbis"'
        url.video = video
        url.save()


if __name__ == '__main__':
    main()

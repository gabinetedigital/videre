# -*- coding: utf-8 -*-
#
# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
# Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Tag(models.Model):
    name = models.CharField(_(u'name'), max_length=300)

    def __unicode__(self):
        return self.name


class Url(models.Model):
    url = models.CharField(_(u'url'), max_length=300)
    content_type = models.CharField(_(u'content type'), max_length=128)
    video = models.ForeignKey('Video', verbose_name=_(u'video'))

    def __unicode__(self):
        return self.url


class Video(models.Model):
    title = models.CharField(_(u'title'), max_length=200)
    creation_date = models.DateTimeField(
        _(u'creation date'), default=datetime.now)
    event_date = models.DateTimeField(_(u'event date'), blank=True, null=True)
    summary = models.TextField(_(u'summary'),)
    author = models.CharField(_(u'author'), max_length=200)
    license_name = models.CharField(_(u'license name'), max_length=200)
    license_link = models.CharField(_(u'license link'), max_length=300)
    thumb_url = models.CharField(_(u'thumb url'), max_length=300, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name=_(u'tags'),)

    def __unicode__(self):
        return self.title

    def as_dict(self):
        """ Returns a dictionary representation of a video object """
        date_handler = lambda x: getattr(x, 'isoformat', lambda:None)()
        return {
            'id': self.id,
            'title': self.title,
            'creation_date': date_handler(self.creation_date),
            'event_date': date_handler(self.event_date),
            'summary': self.summary,
            'author': self.author,
            'license_name': self.license_name,
            'license_link': self.license_link,
            'thumb_url': self.thumb_url,
            'tags': list(self.tags.values_list('name', flat=True)),
            'sources': [{
                    'url': i.url,
                    'content_type': i.content_type,
                    } for i in self.url_set.all()],
        }

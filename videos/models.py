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
    summary = models.TextField(_(u'summary'),)
    author = models.CharField(_(u'author'), max_length=200)
    license_name = models.CharField(_(u'license name'), max_length=200)
    license_link = models.CharField(_(u'license link'), max_length=300)
    thumb_url = models.CharField(_(u'thumb url'), max_length=300, blank=True)
    tags = models.ManyToManyField('Tag', verbose_name=_(u'tags'),)

    def __unicode__(self):
        return self.title

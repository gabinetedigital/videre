# -*- coding: utf-8 -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
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

class Tag(models.Model):
    name = models.CharField(max_length=300)

class Url(models.Model):
    url = models.CharField(max_length=300)
    content_type = models.CharField(max_length=128)
    video = models.ForeignKey('Video')

    def __unicode__(self):
        return self.url

class Video(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    author = models.CharField(max_length=200)
    license_name = models.CharField(max_length=200)
    license_link = models.CharField(max_length=300)
    video_file = models.FileField(upload_to='static/videos')
    thumb_url = models.CharField(max_length=300)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title

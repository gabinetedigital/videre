# -*- coding: utf-8 -*-
#
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

from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.http import HttpResponse
from models import Video

def video(request, vid):
    obj = get_object_or_404(Video, pk=vid)
    callback = request.REQUEST.get('callback')
    dump = dumps({
        'id': obj.id,
        'title': obj.title,
        'summary': obj.summary,
        'author': obj.author,
        'license_name': obj.license_name,
        'license_link': obj.license_link,
        'thumb_url': obj.thumb_url,
        'tags': [i.name for i in obj.tags.all()],
        'sources': [{
            'url': i.url,
            'content_type': i.content_type,
            } for i in obj.url_set.all()],
    })
    content = callback and '%s(%s);' % (callback, dump) or dump
    mimetype = callback and 'text/javascript' or 'application/json'
    return HttpResponse(content, mimetype=mimetype)


def embed(request, vid):
    url = request.build_absolute_uri(reverse('static', args=('',)))
    ctx = {
        'url': url,
        'vid': vid,
        'width': request.GET.get('width', 480),
        'height': request.GET.get('height', 270),
    }
    return render_to_response('embed.html', ctx)

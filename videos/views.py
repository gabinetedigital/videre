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
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.http import HttpResponse
from models import Video


def build_json(request, obj):
    """ Returns an HttpResponse object containing a json data

    If we have the `callback' key present in request, it also prepares
    the response to return JSONP. """
    dump = dumps(obj)
    callback = request.REQUEST.get('callback')
    content = '%s(%s);' % (callback, dump) if callback else dump
    mimetype = 'text/javascript' if callback else 'application/json'
    return HttpResponse(content, mimetype=mimetype)


def video(request, vid):
    """ Returns video data """
    obj = get_object_or_404(Video, pk=vid)
    return build_json(request, obj.as_dict())


def collection(request):
    """ Returns a list of videos, filtered by tag names """
    query = {}

    # This query comes from the request and can contain any text
    search = request.REQUEST.get('q', '')

    # Let's be a bit adaptative. If the user of this API passes
    # something prefixed by a # (%23 if encoded), it will be threated as
    # a tag. Here we have the code that extracts it:
    words = []
    tags = []
    for i in search.split(','):
        if i.startswith('#'):
            tags.append(i[1:])
        else:
            words.append(i)

    # Now, let's search for the found tags
    if tags:
        query.update({'tags__name__in': tags})

    # And here we look for the words in all searchable fields. Currently
    # just title and summary.
    word_search = None
    for word in words:
        if word_search is None:
            word_search = Q(title__icontains=word)
        else:
            word_search |= Q(title__icontains=word)
        word_search |= Q(summary__icontains=word)

    # Let's apply this search and build a json with it and we're done
    if word_search is not None:
        search = Video.objects.filter(word_search, **query)
    else:
        search = Video.objects.filter(**query)
    videos = [i.as_dict() for i in search]
    return build_json(request, videos)


def embed(request, vid):
    """ Returns an html page that renders a player

    It's useful for embeding the video in other pages that you're not
    able to change the html code or add javascript. It also recognizes
    both `width' and `height' variables present in request. """
    api = request.build_absolute_uri(request.META['SCRIPT_NAME'] + '/')
    ctx = {
        'api': api,
        'vid': vid,
        'width': request.GET.get('width', 480),
        'height': request.GET.get('height', 270),
    }
    return render_to_response('embed.html', ctx)


def embed_collection(request):
    """ Returns an html page that renders a collection of videos """
    api = request.build_absolute_uri(request.META['SCRIPT_NAME'] + '/')
    ctx = {
        'api': api,
        'height': request.GET.get('tags', ''),
    }
    return render_to_response('embed_collection.html', ctx)

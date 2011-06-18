/* Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

avl = window.avl || {};
avl.player = (function () {
    function Video (element, opts) {
        opts = opts || {};
        this.$element = $(element);
        this.$element.css({width: this.width, height: this.height});
        this.$element.addClass('video-js-box');

        this.sources = opts.sources;
        this.width = opts.width || 480;
        this.height = opts.height || 270;
        this.setup();
    }

    Video.prototype = {
        setup: function () {
            var $video = $('<video>');
            var uid = 'player-' + (new Date()).getTime();
            var flv = null;
            for (var i = 0; i < this.sources.length; i++) {
                if (this.sources[i].content_type === 'video/x-flv') {
                    flv = this.sources[i].url;
                }

                var attrs = {
                    src: this.sources[i].url,
                    type: this.sources[i].content_type
                };
                $video.append($('<source>').attr(attrs));
            }

            $video.attr({width: this.width, height: this.height});
            $video.addClass('video-js');
            $video
                .append($('<div>').attr('id', uid))
                .appendTo(this.$element);

            /* External library */
            VideoJS.setup($video[0]);

            /* We need to setup flash too */
            if (flv != null) {
                $f(uid, "http://releases.flowplayer.org/swf/flowplayer-3.2.7.swf", {
                    clip: {
                        url: flv,
                        autoPlay: true
                    }
                });
            }
        }
    };

    return function (e, o) { return new Video(e, o); };
})();

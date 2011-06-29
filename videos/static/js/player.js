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

avl.extend('player', function (e, o, disableAsync) {
    function Player (element, opts) {
        opts = opts || {};
        this.sources = opts.sources;
        this.width = opts.width || 480;
        this.height = opts.height || 270;

        /* Configuring the target element */
        this.$element = $(element);
        this.$element.addClass('video-js-box');

        /* Let's build the player */
        this.player();
    }

    Player.prototype = {
        player: function () {
            var $video = $('<video>');
            var uid = 'player-' + (new Date()).getTime();
            var flv = null;
            var rtmp = false;
            for (var i = 0; i < this.sources.length; i++) {
                if (this.sources[i].content_type === 'video/x-flv') {
                    flv = this.sources[i].url;
                    if (this.sources[i].url.substr(0, 4) === 'rtmp') {
                        rtmp = true;
                    }
                }

                var attrs = {
                    src: this.sources[i].url,
                    type: this.sources[i].content_type
                };
                $video.append($('<source>').attr(attrs));
            }

            var $playerContainer = $('<div>').attr('id', uid);
            $playerContainer.css({width: this.width, height: this.height});

            /* Let's the hammer play around
             *
             * There are some special conditions that we have to
             * consider before using the video tag and the flash stuff.
             *
             * I know that these rules are quite basic, and that safari
             * (and other mac stuff) accepts the video tag but not
             * ogg. Here they are:
             *
             *  - (flv && sources.length === 1)
             *  - (flv && ie9)
             *  - (flv && !ogg)
             *  - (flv && chrome) // no metter how it says about chrome
             */
            var videoTag = !!document.createElement('video').canPlayType;
            var ie9 = navigator.userAgent.indexOf("Trident/5") > -1;
            var chrome = navigator.appVersion.indexOf('Chrome') > -1;
            var ogg = false;
            if (videoTag) {
                var v = document.createElement('video');
                ogg = v.canPlayType('video/ogg; codecs="theora, vorbis"');
            }
            if ((this.sources.length === 1 && flv) ||
                (flv && ie9) ||
                (flv && !ogg) ||
                (flv && chrome)) {
                $playerContainer.appendTo(this.$element);
            } else {
                $video.attr({width: this.width, height: this.height});
                $video.addClass('video-js');
                $video.append($playerContainer);
                $video.appendTo(this.$element);
            }

            /* Setting up video js in the just added player. It will not
             * until we add it to the dom structure */
            VideoJS.setup($('video', this.$element)[0]);

            /* We need to setup flash too */
            if (flv != null) {
                var cfg = {
                    clip: {
                        url: flv,
                        autoPlay: true
                    }
                };

                /* We also need to support flash streaming */
                if (rtmp) {

                    /* Handling requests in all styles, including akamai
                     * ones.
                     *
                     * Don't know why they just don't use another
                     * mimetype once they're not actually providing flv
                     * content in the first request... */
                    var result = /^(.+)\/([^\/]+)$/.exec(flv);
                    var netConnectionUrl = result[1];
                    var clipUrl = result[0]

                    cfg.clip.url = clipUrl;
                    cfg.clip.live = true;
                    cfg.clip.provider = 'influxis';
                    cfg.plugins = {
                        influxis: {
                            url: 'http://releases.flowplayer.org/swf/flowplayer.rtmp-3.2.3.swf',
                            netConnectionUrl: netConnectionUrl
                        }
                    };
                }

                $f(uid, "http://releases.flowplayer.org/swf/flowplayer-3.2.7.swf", cfg);
            }
            return $video;
        }
    };

    /* We shall want to call this API with the video object already
     * loaded */
    if (disableAsync === true) {
        return new Player(e, o);
    }

    /* Ok, let's proced with the async call */
    $.getJSON(this.api_url + '/' + o.id + '/?callback=?', function (video) {
        /* Updating the video object with params passed in the `opts'
         * param. */
        for (var i in o) {
            video[i] = o[i];
        }
        new Player(e, video);
    });
});

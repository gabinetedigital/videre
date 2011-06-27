/* Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
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

avl.extend('collection', function (e, o) {
    var thumbTemplate =
        '<li>' +
        '  <a href="{link}"><img src="{thumb_url}" alt="{title}"></a>' +
        '  <dl class="info">' +
        '    <dd class="date">{date}</dd>' +
        '    <dd class="hour">{hour}</dd>' +
        '  </dl>' +
        '  <p>{summary}</p>' +
        '</li>';

    function Collection(element, opts) {
        this.opts = opts || {};

        /* Callback fired when clicking a video */
        this.videoCallback = typeof opts.videoCallback === 'function' ?
            opts.videoCallback : function (obj) { };

        /* List of items to be shown */
        this.items = opts.items;

        /* Visual stuff: first, we get the element that will be the
         * targed of our collection rendering and then we render it! */
        this.$element = $(element);
        this.render();
    }

    Collection.prototype = {
        render: function () {
            var $ul = $('<ul>').addClass('collection');
            for (var i = 0; i < this.items.length; i++) {
                $ul.append(this.render_video(this.items[i]));
            }
            $ul.appendTo(this.$element);
        },

        render_video: function (video) {
            var date;
            var dateObj = new Date(video.event_date);
            if (typeof this.opts.dateFormat === 'function') {
                date = this.opts.dateFormat(dateObj);
            } else {
                var year = dateObj.getYear();
                year = year < 1900 ? year + 1900 : year;

                var month = avl.zfill(dateObj.getMonth()+1, 2);
                date = year + '/' + month + '/' + dateObj.getDate();
            }

            var hour = dateObj.getHours() + ':' + dateObj.getMinutes();

            var $li = $(avl.tmpl(thumbTemplate, {
                'link': '#' + video.id,
                'thumb_url': video.thumb_url,
                'title': video.title,
                'summary': video.summary,
                'date': date,
                'hour': hour
            }));

            var context = this;
            $('a', $li).click(function (evt) {
                context.opts.videoCallback(evt, video);
            });
            return $li;
        }
    };

    $.getJSON(this.api_url + '/?callback=?', function (collection) {
        var opts = o || {};
        opts.items = collection;
        new Collection(e, opts);
    });
});

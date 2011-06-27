/* Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
 * Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
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

var avl = (function () {
    function Avl() {
        this.api_url = null;
    }

    Avl.prototype = {
        init: function (api_url) {
            this.api_url = api_url;
        },

        extend: function (name, plugin) {
            this[name] = plugin;
        }
    };

    return new Avl();
})();

/* Our micro javascript library :) */

/** This small function just replaces { var } ocorrences by the `var'
 * value present in the `context' object.
 *
 * @param {String} content is the string that will have the `variables'
 * replaced
 *
 * @param {Object} context is the object that contains the keys and
 * values of variables.
 */
avl.extend('tmpl', function (s, context) {
    s = '' + s;
    for (var i in context) {
        var reg = new RegExp('\{\s*' + i + '\s*\}');
        s = s.replace(reg, context[i]);
    }
    return s;
});


/** Fills the string with `n' zeros at left
 *
 * @param {String} s is the string to be filled out
 * @param {Number} n is the final size of the whole string
 */
avl.extend('zfill', function (s, n) {
    s = '' + s;
    while (s.length < n) {
        s = '0' + s;
    }
    return s;
});

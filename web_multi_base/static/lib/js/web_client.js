odoo.define('web_multi_base.web_client', function(require) {
"use strict";

    var AbstractWebClient = require('web.AbstractWebClient');
    AbstractWebClient.prototype._onPushState = function (e) {
        var state = $.bbq.getState();
        this.do_push_state(_.extend(e.data.state, {'cids': state.cids, 'wids': state.wids}));
    };
});

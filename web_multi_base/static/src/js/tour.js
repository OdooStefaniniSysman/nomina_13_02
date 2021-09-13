odoo.define("web_multi_base.tour", function(require) {
    "use strict";

    var tour = require("web_tour.tour");

    var options = {
        test: true,
        url: "/web#",
    };

    var tour_name = "web_multi_base.tour";
    tour.register(tour_name, options, [
        {
            content: "Toggle Website Switcher",
            trigger: ".o_switch_website_menu > a",
            extra_trigger: ".o_mail_discuss_sidebar",
        },
        {
            content: "Click My Website",
            trigger: ".o_switch_website_menu div[data-website-id=1]",
        },
    ]);
});

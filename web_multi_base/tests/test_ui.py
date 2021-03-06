from odoo.tests import common, tagged


@tagged("at_install", "post_install")
class TestUI(common.HttpCase):
    def test_ui(self):
        # needed because tests are run before the module is marked as
        # installed. In js web will only load qweb coming from modules
        # that are returned by the backend in module_boot. Without
        # this you end up with js, css but no qweb.
        phantom_env = self.env
        phantom_env["ir.module.module"].search(
            [("name", "=", "web_multi_base")], limit=1
        ).state = "installed"
        demo_user = phantom_env.ref("base.user_demo")

        # Reset user's values
        demo_user.company_id = self.env.ref("base.main_company")
        demo_user.website_id = None
        demo_user.access_backend_website_ids = None

        tour = "web_multi_base.tour"
        self.phantom_js(
            "/web",
            "odoo.__DEBUG__.services['web_tour.tour'].run('%s')" % tour,
            "odoo.__DEBUG__.services['web_tour.tour'].tours['%s'].ready" % tour,
            login="demo",
        )

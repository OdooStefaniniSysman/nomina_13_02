# -*- coding: utf-8 -*-

from . import models

from odoo import api


def pre_init_hook(cr):
    cr.execute("""ALTER TABLE res_partner ADD COLUMN email_before character varying;""")
    cr.execute("""UPDATE res_partner SET email_before = email;""")
    cr.execute("""ALTER TABLE res_users ADD COLUMN signature_before text;""")
    cr.execute("""UPDATE res_users SET signature_before = signature;""")

def post_init_hook(cr, registry):
    cr.execute("""INSERT INTO res_partner_email (company_id, partner_id, email) SELECT company_id, id, email_before FROM res_partner where company_id IS NOT NULL;""")
    cr.execute("""ALTER TABLE res_partner DROP COLUMN email_before;""")
    # cr.execute("""INSERT INTO res_users_signature (company_id, user_id, signature) SELECT company_id, id, signature_before FROM res_users where company_id IS NOT NULL;""")
    # cr.execute("""ALTER TABLE res_users DROP COLUMN signature_before;""")

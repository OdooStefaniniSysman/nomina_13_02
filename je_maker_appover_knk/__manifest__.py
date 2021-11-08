# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
#################################################################################

{
    'name': 'Journal Entries Maker Approver kanak',
    'version': '1.0',
    'description': """
    manage journal entries in invoicing
    """,
    'summary': 'This module allow to manage journal entries in invoicing.',
    'category': 'Accounting',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'depends': ['base', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/account_move.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'sequence': 1,
    'installable': True,
    'application': True,
}

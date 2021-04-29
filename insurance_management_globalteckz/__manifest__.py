 # -*- coding: utf-8 -*-
##############################################################################
#
#    Globalteckz Pvt Ltd
#    Copyright (C) 2013-Today(www.globalteckz.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Insurance Management by Globalteckz',
    'version': '0.1',
    'category': 'Insurance Management',
    'sequence': 2,
    'summary': 'Insurance Policy management in Odoo 14 manage insurance management which include insurance customers with payment details of premium.Ha',
    'description': '''
Insurance Management is to maintain all policy details based on EMI provided.

                    ''',
    'website': 'http://www.globalteckz.com/',
    'author': 'Globalteckz',
    "license" : "Other proprietary",
    'images': ['static/description/insurance_banner.png'],
    "price": "99.00",
    "currency": "EUR",
    'depends': ['base','account','sale'],
    'data': [
            'security/policy_security.xml',
            'security/ir.model.access.csv',
            'views/insurance_view.xml',
            'views/insurance_banch_view.xml',
            'views/agent_view.xml',
            'views/policy_view.xml',
            'views/sale_policy_view.xml',
            'views/customer_view_inherit.xml',
            'views/ins_scheduler.xml',
            'report/policy_sale_template.xml',
            'report/reports_view.xml',
            'report/policy_email_template.xml',
            # 'sale_policy_workflow.xml',

            ],
    'demo': ['data/demo_data.xml'],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

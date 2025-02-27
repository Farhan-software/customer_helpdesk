# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Support",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Farhan Ahamed",
    'website': "https://www.xyz.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'website'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/helpdesk_report_view.xml',
    ],
    'icon': '/customer_helpdesk/static/description/icon.png',

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

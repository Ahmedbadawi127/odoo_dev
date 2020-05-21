# -*- coding: utf-8 -*-
{
    'name': "lab",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ahmed Badawi",
    'website': "http://www.GoBadawi.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'version': '0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        'security/lab_security.xml',
        'views/lab_reports.xml',
        'views/tempates.xml',
        'views/lab_cases_between_Dates_wiz.xml',
        'data/ir_sequence_data.xml',
        'views/lab_agencies_doctors.views.xml',
        'views/lab_operations_cases.views.xml',
        'views/lab_settings.xml',
        'views/lab_states.xml',
        'views/lab_materials.views.xml',
        'views/lab_diagnosis.views.xml',
        'views/menus.xml',

    ],


}

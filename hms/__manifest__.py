{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'description': 'Hospital Management System',
    'depends': ['base'],
    'data': [
        'security/hms_security.xml',
        'security/ir.model.access.csv',
        'views/hms_views.xml',
        'views/hms_department_view.xml',
        'views/hms_doctors_view.xml',
        'views/res_partner_view.xml',
        'report/hms_patient_report.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
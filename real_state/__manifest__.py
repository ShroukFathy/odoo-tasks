{
    'name': 'Real State',
    'version': '1.0',
    'summary': '',
    'description': "Longer description of what this module does.",
    'author': 'Your Name / Company',
    'depends': ['base', 'mail','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
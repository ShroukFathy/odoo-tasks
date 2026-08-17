{
    'name': 'Cost Estimate',
    'version': '1.0',
    'description': 'Project cost estimate',
    'depends': ['base', 'mail','project'],
    'data': [
        'security/project_cost_estimate_security.xml',
        'security/ir.model.access.csv',
        'views/project_cost_estimate.xml',
        'views/project_cost_breakdown.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
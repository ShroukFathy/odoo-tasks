{
    'name': 'Cost Estimate',
    'version': '1.0',
    'description': 'Project cost estimate',
    'depends': ['base', 'mail','project','product'],
    'data': [
        'security/project_cost_estimate_security.xml',
        'security/ir.model.access.csv',
        'data/cst_estimate_esequence.xml',
        'views/project_cost_estimate.xml',
        'views/project_project_view.xml',
        'views/project_cost_estimate_history_view.xml',
        'wizard/rejection_reason_wizard_view.xml',
        'views/res_config_settings.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
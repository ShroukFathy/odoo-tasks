{
    'name': 'To-Do List',
    'version': '1.0',
    'description': 'To-do Management',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/todo_view.xml',
        'report/todo_task_report.xml',
        'views/todo_history_view.xml',
        'wizard/change_state_wizard_view.xml'

    ],
    'assets' : {
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
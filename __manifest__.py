{
    'name': 'School Management System',
    'version': '19.0.1.0.0',
    'summary': 'Manage students and school operations',
    'description': """
        School Management System
        ========================
        Features:
        - Student registration
        - Student information management
        - Student search and filtering
    """,
    'category': 'Education',
    'author': 'Ahmed Omran',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
    ],
    'application': True,
    'installable': True,
}
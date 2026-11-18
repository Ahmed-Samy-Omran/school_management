{
    'name': 'School Management System',
    'version': '19.0.1.1.0',
    'summary': 'Manage students and school operations',
    'description': """
        School Management System
        ========================
        Features:
        - Student registration and management
        - Teacher registration and management
        - Computed age and years of service
        - Email, date and uniqueness validations
        - Search, filters and grouping
    """,
    'category': 'Education',
    'author': 'Ahmed Omran',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/teacher_views.xml',
    ],
    'application': True,
    'installable': True,
}
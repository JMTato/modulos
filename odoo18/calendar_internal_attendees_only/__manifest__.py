{
    'name': 'Calendar: Only Internal Users as Attendees',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Limit calendar attendees to internal users for specific user group',
    'depends': ['calendar'],
    'data': [
        'security/security.xml',
        'views/calendar_event_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
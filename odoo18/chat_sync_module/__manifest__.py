{
    'name': 'Chat Sync Module',
    'version': '1.0',
    'summary': 'Sincronización de grupos de chat entre Odoo locales y clientes.',
    'author': 'North Atlantic Consulting',
    'website': 'https://www.northatlanticconsulting.com',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'views/chat_group_views.xml',
        'views/menu_items.xml',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': True,
}
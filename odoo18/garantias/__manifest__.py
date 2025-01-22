# __manifest__.py
{
    'name': 'Garantías',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Gestión de garantías de equipos',
    'description': """
    Módulo para registrar las garantías de los equipos instalados por técnicos.
    """,
    'author': 'North Atlantic Consulting LLC',
    'website': 'https://atlanticonorteconsultores.com',
    'depends': [
        'base',
        'web',
        # Si necesitas otros módulos de Odoo, agrégalos aquí
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/garantias_menus.xml',
        'views/garantias_views.xml',
        'views/garantias_map_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'garantias/static/src/js/garantia_map.js',
        ],
    },
    'installable': True,
    'application': True,
}
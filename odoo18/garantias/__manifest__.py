# __manifest__.py
{
    'name': 'Garantías',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Gestión integral de garantías para equipos instalados',
    'description': """
        Este módulo permite a las empresas gestionar garantías de los equipos 
        instalados, llevar un seguimiento de los reclamos, tiempos de garantía, 
        y registro de actividades realizadas por los técnicos en cada servicio.
    """,
    'author': 'North Atlantic Consulting LLC',
    'website': 'https://atlanticonorteconsultores.com',
    'depends': [
        'base',
        'web',
        # Si necesitas otros módulos de Odoo, agrégalos aquí
    ],
    'data': [
        'security/garantias_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/garantias_menus.xml',
        'views/garantias_views.xml',
        'views/garantias_map_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'garantias/static/src/js/garantias_map.js',
            'garantias/static/src/xml/garantias_map_template.xml',
            'garantias/static/src/css/garantias_map.css',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
        ],
        'web.assets_qweb': [
            # Si tienes archivos XML o plantillas frontend
        ],
    },
    'images': [
        'garantias/static/img/default_icon_app.png'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
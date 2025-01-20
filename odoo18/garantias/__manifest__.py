{
    'name': 'Gestión de Garantías',
    'version': '1.0',
    'summary': 'Registro de garantías de equipos instalados',
    'category': 'Custom',
    'author': 'North Atlantic Consulting LLC',
    'website': 'https://atlanticonorteconsultores.com',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/garantias_view.xml',
    ],
    'installable': True,
    'application': True,
}
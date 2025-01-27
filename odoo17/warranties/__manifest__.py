{
    'name': 'Warranties',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Product Warranties Management',
    'description': """
        Module for managing product warranties with customer information and geolocation.
    """,
    'depends': ['base', 'base_geolocalize'],
    'data': [
        'security/warranty_security.xml',
        'security/ir.model.access.csv',
        'data/warranty_sequence.xml',
        'views/warranty_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
{
    'name': "tyre extra fields",
    'version': '17.0.1.0.0',
    'summary': "Agrega los campos Eficiencia Combustible, Agarre Mojado y Ruido a la ficha de producto",
    'description': """
Módulo para Odoo 17 que añade tres campos adicionales en la ficha del producto:
    - Eficiencia Combustible
    - Agarre Mojado
    - Ruido
""",
    'category': 'Product',
    'author': "North Atlantic Consulting LLC",
    'website': "http://atlanticonorteconsultores.com",
    'depends': ['product'],
    'data': [
        'views/product_template_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

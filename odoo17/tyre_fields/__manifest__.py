{
    "name": "Tyre Fields en productos",
    "version": "1.0",
    "summary": "Agregar campos Eficiencia Combustible, Agarre Mojado y Ruido a la ficha del producto",
    "description": "Este módulo añade tres campos personalizados relacionados con neumáticos en la ficha de productos.",
    "author": "North Atlantic Consulting",
    "depends": ["product", "sale", "account"],
    "data": [
        "views/product_template_views.xml",
        "views/sale_order_line_views.xml",
        "views/sale_order_report_views.xml",
        'views/account_move_report_views.xml',
        'views/account_move_form_views.xml',
        'views/account_move_line_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tyre_fields/static/src/css/style.css',
        ],
    },
    "installable": True,
    "application": False,
}

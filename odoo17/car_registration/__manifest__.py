{
    "name": "Vehículos en Pedidos de Venta",
    "summary": "Agrega un campo desplegable en ventas con los vehículos del cliente",
    "version": "17.0.1.0.0",
    "author": "North Atlantic Consulting LLC",
    "website": "https://atlanticonorteconsultores.com",
    "depends": ["sale_management", "fleet"],
    "category": "Sales",
    "license": "LGPL-3",
    "data": [
        "views/sale_order_views.xml",
        "views/res_partner_views.xml",
        "views/report_saleorder.xml",
    ],
    "installable": True,
    "application": False,
}
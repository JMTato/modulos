{
    "name": "Gestión de Vehículos en Pedidos y Facturas",
    "summary": "Agrega los campos Vehículo (enlazado con el módulo de flota), Matrícula y Kilómetros a los presupuestos/pedidos y a las facturas",
    "version": "17.0.1.0.0",
    "author": "North Atlantic Consulting LLC",
    "website": "https://atlanticonorteconsultores.com",
    "depends": [
        "sale_management",  # Depende de Ventas
        "account",  # Depende de Contabilidad (para facturas)
        "fleet",  # Asegura que Flota esté instalado antes
    ],
    "category": "Sales",
    "license": "LGPL-3",
    "data": [
        "views/sale_order_views.xml",
        "views/res_partner_views.xml",
        "views/report_saleorder.xml",
        "views/portal_sale_order.xml",
        "views/account_move_views.xml",
        "views/report_invoice.xml",
    ],
    "installable": True,
    "application": False,
}
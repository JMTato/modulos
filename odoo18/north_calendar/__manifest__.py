{
    "name": "North Calendar",
    "version": "1.0",
    "summary": "Filtra partner_ids para usuarios internos en calendario",
    "description": """
North Calendar
==============

Este módulo extiende el módulo de Calendario en Odoo 18 Community para limitar la selección del campo `partner_ids` (participantes del evento) únicamente a usuarios internos (no compartidos) del sistema.

Características:
----------------
- Agrega un grupo de seguridad llamado "Solo ver usuarios internos en calendario".
- Solo los usuarios que pertenezcan a este grupo verán filtrado el campo `partner_ids`.
- El filtro aplicado muestra únicamente partners vinculados a usuarios internos (`res.users`) que no sean usuarios compartidos (`share=False`).
- No afecta a otros usuarios que no estén en el grupo.

Uso:
----
- Instalar el módulo.
- Asignar el grupo "Solo ver usuarios internos en calendario" a los usuarios deseados.
- Al crear o editar un evento de calendario, el campo `partner_ids` solo mostrará usuarios internos.
""",
    "category": "Calendar",
    "author": "Tu Nombre",
    "depends": ["calendar"],
    "data": [
        "security/north_calendar_groups.xml",
        "views/calendar_event_view.xml"
    ],
    "installable": True,
    "application": False
}

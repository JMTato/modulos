from odoo import models, api
from odoo.exceptions import ValidationError

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    @api.constrains('partner_ids')
    def _check_only_internal_users_as_attendees(self):
        restricted_group = self.env.ref('calendar_internal_attendees_only.group_calendar_internal_attendees_only')
        for event in self:
            if restricted_group in self.env.user.groups_id:
                for partner in event.partner_ids:
                    if not partner.user_ids:
                        raise ValidationError("Solo puedes añadir usuarios internos como asistentes.")
                    for user in partner.user_ids:
                        if user.share or user.has_group('base.group_portal'):
                            raise ValidationError("Solo puedes añadir usuarios internos como asistentes.")
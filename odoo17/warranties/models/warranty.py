from odoo import models, fields, api, _

class ProductWarranty(models.Model):
    _name = 'product.warranty'
    _description = 'Product Warranty'
    _rec_name = 'reference'

    reference = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        default=lambda self: _('New')
    )
    registration_date = fields.Date(
        string='Registration Date',
        default=fields.Date.context_today,
        required=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    customer_name = fields.Char(
        string='Full Name',
        required=True
    )
    vat = fields.Char(
        string='NIF',
        required=True
    )
    mobile = fields.Char(
        string='Mobile',
        required=True
    )
    street = fields.Char(
        string='Street',
        required=True
    )
    city = fields.Char(
        string='City',
        required=True
    )
    state_id = fields.Many2one(
        'res.country.state',
        string='Province',
        required=True
    )
    zip = fields.Char(
        string='ZIP Code',
        required=True
    )
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        required=True
    )
    location = fields.Char(
        string='Location',
        compute='_compute_location',
        store=True
    )
    partner_latitude = fields.Float(
        string='Latitude',
        digits=(16, 5)
    )
    partner_longitude = fields.Float(
        string='Longitude',
        digits=(16, 5)
    )
    barcode = fields.Char(
        string='Barcode',
        required=True
    )
    serial_number = fields.Char(
        string='Serial Number',
        required=True
    )
    device_photo = fields.Binary(
        string='Device Photo',
        required=True,
        attachment=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('product.warranty') or _('New')
        return super().create(vals_list)

    @api.depends('street', 'city', 'state_id', 'zip', 'country_id')
    def _compute_location(self):
        for warranty in self:
            location_parts = [
                warranty.street,
                warranty.city,
                warranty.state_id.name if warranty.state_id else False,
                warranty.zip,
                warranty.country_id.name if warranty.country_id else False
            ]
            warranty.location = ', '.join(filter(None, location_parts))

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(
            street=street,
            zip=zip,
            city=city,
            state=state,
            country=country
        )
        result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        for warranty in self:
            result = self._geo_localize(
                street=warranty.street,
                zip=warranty.zip,
                city=warranty.city,
                state=warranty.state_id.name,
                country=warranty.country_id.name
            )
            if result:
                warranty.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1]
                })
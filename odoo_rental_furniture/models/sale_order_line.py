from odoo import fields, models, api
from odoo.tools import format_amount


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_rental = fields.Boolean(compute='_compute_is_rental', store=True, precompute=True)
    is_product_rentable = fields.Boolean(related='product_id.rent_ok', depends=['product_id'])

    @api.depends('product_id')
    def _compute_is_rental(self):
        for line in self:
            line.is_rental = line.is_product_rentable

    rent_price_on_day = fields.Float(
        string="Rent Price (Per Day)",
        help="Rent price for single day.",
        compute="_compute_rent_price_on_day"
    )

    display_rental_price = fields.Float(
        string="Total Rental price",
        compute='_compute_display_price',
        help="First rental pricing of the product",
        readonly=False,
        store=True
    )

    @api.depends('product_id', 'rent_price_on_day', 'order_id.duration_days', 'product_id.rent_price_on_day',
                 'product_uom_qty')
    def _compute_display_price(self):
        for rec in self:
            rec.display_rental_price = rec.rent_price_on_day * rec.order_id.duration_days * rec.product_uom_qty

    @api.depends('product_id', 'product_id.rent_price_on_day')
    def _compute_rent_price_on_day(self):
        for rec in self:
            if rec.product_template_id:
                rec.rent_price_on_day = rec.product_template_id.rent_price_on_day
                # if product is rental then keep price unit 0 to balance the account.
                if rec.product_template_id.rent_ok:
                    rec.write({'price_unit': 0,
                               'price_subtotal': rec.product_uom_qty * rec.display_rental_price
                               })
            else:
                rec.rent_price_on_day = 0

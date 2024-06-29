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
        default=10
    )

    display_rental_price = fields.Char(
        string="Total Rental price",
        compute='_compute_display_price',
        help="First rental pricing of the product",
    )

    @api.depends('product_id', 'rent_price_on_day', 'order_id.duration_days', 'product_id.rent_price_on_day')
    def _compute_display_price(self):
        self.display_rental_price = self.rent_price_on_day * self.order_id.duration_days * self.product_uom_qty

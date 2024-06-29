from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_rental = fields.Boolean(compute='_compute_is_rental', store=True, precompute=True)
    is_product_rentable = fields.Boolean(related='product_id.rent_ok', depends=['product_id'])

    @api.depends('product_id')
    def _compute_is_rental(self):
        for line in self:
            line.is_rental = line.is_product_rentable

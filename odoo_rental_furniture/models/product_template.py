# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rent_ok = fields.Boolean(
        string="Can be Rented",
        help="Allow renting of this product.")



# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Rental Furniture",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "author": "",
    "summary": "Rental Customisation",
    "description": """
    
    """,
    "website": "",
    'depends': ['sale', 'sale_management', 'calendar'],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
}

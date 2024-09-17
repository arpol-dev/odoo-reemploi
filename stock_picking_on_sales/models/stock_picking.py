# Copyright 2024 ArPol
# @author: Armand Polmard <armand@arpol.fr>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
import datetime
import logging


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    code = fields.Selection(selection_add=[("from_sale", "Collecte")], ondelete={"from_sale": "cascade"})
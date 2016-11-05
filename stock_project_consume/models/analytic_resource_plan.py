# -*- coding: utf-8 -*-
# <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AnalyticResourcePlanLine(models.Model):
    _name = "analytic.resource.plan.line"
    _description = "Resource Plan"
    _inherit = "analytic.resource.plan.line"

    qty = fields.Float(string="Quantity Planned")
    qty_on_hand = fields.Float(
        string="Quantity on Hand",
        compute="_compute_qty_on_hand",
        )
    qty_consumed = fields.Float(
        string="Quantity Consumed",
        compute="_compute_qty_consumed")

    @api.multi
    def _compute_qty_on_hand(self):
        for rec in self:
            products = self.env['stock.quant'].search(
                [('product_id', '=', rec.product_id.id),
                 ('location_id', '=',
                    rec.task_resource_id.project_id.location_id.id)])
            if products:
                for product in products:
                    rec.qty_on_hand += product.qty

    @api.multi
    def _compute_qty_consumed(self):
        for rec in self:
            products = self.env['stock.move'].search(
                [('product_id', '=', rec.product_id.id),
                 ('location_id', '=',
                    rec.task_resource_id.project_id.location_id.id),
                 ('location_dest_id', '=',
                    rec.task_resource_id.project_id.
                    picking_out_id.default_location_dest_id.id),
                 ('state', '=', 'done')])
            if products:
                for product in products:
                    rec.qty_consumed += product.product_uom_qty
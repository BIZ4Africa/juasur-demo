from odoo import models, fields, api, _, exceptions

class purchase_requisition(models.Model):
    _inherit = ['crm.lead']

    purchase_requisition_count = fields.Integer(string='purchase requisition', compute='_purchase_requisition_count', store=False)
    # purchase_requisition_ids = fields.One2many('purchase.requisition', 'lead_id', string='purchase requisition IDs', copy=False)

    def _purchase_requisition_count(self):
        for subscription in self:
            subscription.pms_sale_order_count = self.env['purchase.requisition'].search_count(
                [])

    def action_purchase_requisition(self):
        self.ensure_one()
        purchase_requisition = self.env['purchase.requisition'].search([()])
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.requisition",
            "views": [[False, "kanban"], [False, "list"], [False, "form"], ],
            "domain": [],
            "context": {"create": True,},
            "name": _("purchase_requisition"),
        }

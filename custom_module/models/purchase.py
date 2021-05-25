from odoo import models, fields, api, _, exceptions

class purchase_requisition(models.Model):
    _inherit = ['purchase.requisition']

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

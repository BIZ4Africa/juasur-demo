 # -*- coding: utf-8 -*-
##############################################################################
#
#    Globalteckz Pvt Ltd
#    Copyright (C) 2013-Today(www.globalteckz.com).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models ,api, _
from datetime import  datetime

class Agent_details(models.Model):

    _name = "res.partner"
    _inherit = ['res.partner', 'mail.thread']

    dob = fields.Date(string='Date Of Birth' ,track_visibility='onchange')
    branch_name= fields.Many2one('res.company',string='Branch', track_visibility='onchange')
    is_agent = fields.Boolean('Agent', default=False,readonly=True ,track_visibility='onchange')
    agent_code = fields.Char(string='Agent Code',readonly=True ,track_visibility='onchange')
    policy_list = fields.One2many('sale.policy', 'policy_holder', string='Policy List')

    @api.model
    def create(self,vals):
        print('vals-----------------',vals)
        print('self._context-----------------',self._context)
        if self._context.get('is_agent'):
            vals.update({'is_agent': True})
            sequence = self.env['res.company'].browse(vals['branch_name']).sq_id
            if sequence:
                vals.update({'agent_code': sequence.next_by_id(),})
        return super(Agent_details, self).create(vals)





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
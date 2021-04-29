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
from odoo.exceptions import UserError, ValidationError
from datetime import  datetime
from datetime import  timedelta
from dateutil.relativedelta import relativedelta

class sale_policy(models.Model):
    _name = 'sale.policy'
    _rec_name = 'policy_number'
    _inherit = 'mail.thread'

    policy_holder = fields.Many2one('res.partner',string='Policy Holder Name' ,states={'done':[('readonly',True)]} ,required=True , track_visibility='onchange')
    policy_number = fields.Char(string='Policy number',readonly=True ,states={'done':[('readonly',True)]} , track_visibility='onchange')
    policy_term = fields.Many2one('account.payment.term', string='Payment Term',required=True ,states={'done':[('readonly',True)]} , track_visibility='onchange')
    policy_schemes = fields.Many2one('schemes.details', string='Policy Scheme Name' ,required=True,states={'done':[('readonly',True)]} , track_visibility='onchange')
    branch_name= fields.Many2one('res.company',string='Branch' ,states={'done':[('readonly',True)]} , track_visibility='onchange')
    agent_name = fields.Many2one('res.partner',string='Agent name' ,states={'done':[('readonly',True)]} , track_visibility='onchange')
    duration = fields.Integer(string = 'Duration in Year:' ,required=True,states={'done':[('readonly',True)]})
    issu_date = fields.Date(string='Policy Issu Date' ,required=True,states={'done':[('readonly',True)]})
    end_date = fields.Date(compute="policy_issudate",store='True',string='Policy End Date',readonly=True )
    emi = fields.Selection([
        ('12', 'Monthly'),
        ('4', 'Quarterly'),
        ('2', 'Half Yearly'),
        ('1', 'Yearly')], string='Premium Type' ,required=True,states={'done':[('readonly',True)]})
    policy_amount= fields.Integer(string='Policy Amount' ,required=True,states={'done':[('readonly',True)]})
    state = fields.Selection([
            ('new', 'New'),
            ('confirm', 'Confirm'),
            ('cancel', 'Cancelled'),
            ('done', 'Done')], string='State',default='new', readonly=True, track_visibility='onchange')
    emi_line_ids = fields.One2many('policy.emi.line','sale_policy_id',string='Policy Line Ids')


    def confirm_btn(self):
        self.state = "confirm"

    @api.depends('duration','issu_date')
    def policy_issudate(self):
        addyears = self.duration
        if type(self.issu_date) is bool:
            return
        mydate = datetime.strptime(str(self.issu_date), "%Y-%m-%d").date()
        self.end_date = mydate + relativedelta(years=addyears,days=-1)

    @api.onchange('policy_amount')
    def onchange_duration(self):
        min_amount = self.policy_schemes.min_amount
        max_amount = self.policy_schemes.max_amount
        policy_amount = self.policy_amount

        if policy_amount < min_amount and policy_amount > max_amount:
            raise ValidationError(_('Policy amount is Not Between %s  to %s ') % (min_amount, max_amount))

    
    def msg_amount(self):
        min_amount = self.policy_schemes.min_amount
        max_amount = self.policy_schemes.max_amount

        return ('Policy amount is Not Between %s  to %s ') % (min_amount,max_amount)


    def check_policy_amount(self):
        min_amount = self.policy_schemes.min_amount
        max_amount = self.policy_schemes.max_amount
        policy_amount = self.policy_amount

        if policy_amount < min_amount or policy_amount > max_amount:
            return False
        return True


    @api.onchange('duration')
    def onchange_duration(self):
        min_duration = self.policy_schemes.min_duration
        max_duration = self.policy_schemes.max_duration
        duration = self.duration
        if duration < min_duration or duration > max_duration:
            raise UserError(_('Policy Duration is Not Between %s Year to %s Year ') % (min_duration, max_duration))

    def msg_duration(self):
        min_duration = self.policy_schemes.min_duration
        max_duration = self.policy_schemes.max_duration
        return ('Policy Duration is Not Between %s Year to %s Year ') % (min_duration, max_duration)


    def check_policy_duration(self):

        min_duration = self.policy_schemes.min_duration
        max_duration = self.policy_schemes.max_duration
        policy_duration = self.duration

        if policy_duration < min_duration or policy_duration > max_duration:
            return False
        return True

    # _constraints = [(check_policy_amount, msg_amount, ["policy_amount"]),(check_policy_duration, msg_duration, ["duration"])]


    @api.depends('duration','policy_amount','emi')
    def create_emi_line(self):
        print (":::::::::::::::::::::::::::::::::::::::::::::::Cakkeeee")
        sequence = self.policy_schemes.sq_id
        self.write({
            'policy_number': sequence.next_by_id(),
            'state': 'done',
        })

        total_emi =int(self.duration) * int(self.emi)
        per_emi_amount =float(self.policy_amount) / float(total_emi)
        per_emi_amount =round(per_emi_amount, 2)

        if type(self.issu_date) is bool:
            return
        mydate = datetime.strptime(str(self.issu_date), "%Y-%m-%d").date()

        if self.emi=='12':
            add_months =1
        elif self.emi == '4':
            add_months = 3
        elif self.emi == '2':
            add_months = 6
        elif self.emi == '1':
            add_months = 12

        for i in range(1,total_emi+1):
            emi_start_date = mydate
            emi_end_date = emi_start_date + relativedelta(months=add_months, days=-1)
            mydate = emi_end_date + relativedelta(days=1)

            emi_liens = {
                'sale_policy_id': self.id,
                'emi_no': i,
                'emi_start_date':  emi_start_date,
                'emi_end_date': emi_end_date,
                'emi_amount': per_emi_amount

            }
            emi_line_id = self.env['policy.emi.line'].create(emi_liens)

    @api.model
    def create_policy_number(self):
        sequence = self.policy_schemes.sq_id
        self.write({
            'policy_number': sequence.next_by_id(),
        })
        return True


    def view_policy_invoice(self):

        action = self.env.ref('account.action_move_out_invoice_type')
        form = self.env.ref('account.view_move_form', False)
        form_id = form.id if form else False
        tree = self.env.ref('account.invoice.tree', False)
        tree_id = tree.id if tree else False
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            # 'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }

        pick_ids = []
        for line in self.emi_line_ids:
            if line.invoice_id:
                pick_ids += [line.invoice_id.id]

        if len(pick_ids) > 1:
            result['domain'] = "[('id','in'," + str(pick_ids) + ")]"
            result['views'] = [(tree_id, 'tree'), (form_id, 'form')]

        elif len(pick_ids) == 1:
            result['views'] = [(form_id, 'form'), (tree_id, 'tree')]
            result['res_id'] = pick_ids[0]
        return result


    def send_mail_by_wizard(self):
        if self.policy_holder.email == False:
            raise UserError(_("Please add %s's Email addres for send email ") % (self.policy_holder.name))
        else:
            self.ensure_one()
            template = self.env.ref('old_insurance_management.email_template_policy_details', False)
            compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)

            ctx = dict(
                default_model='sale.policy',
                default_res_id=self.id,
                default_use_template=bool(template),
                default_template_id=template and template.id or False,
                default_composition_mode='comment',
            )
            return {
                    'name': _('Compose Email'),
                    'type': 'ir.actions.act_window',
                    # 'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'mail.compose.message',
                    'views': [(compose_form.id, 'form')],
                    'view_id': compose_form.id,
                    'target': 'new',
                    'context': ctx,
                    }

class policy_emi(models.Model):

    _name = 'policy.emi.line'
    _description = 'policy.emi.line'
    
    sale_policy_id = fields.Many2one('sale.policy',string='Poliocy Id')
    emi_no = fields.Integer(string='Emi No',readonly=True)
    emi_start_date = fields.Date(string='From Date', readonly=True)
    emi_end_date = fields.Date(string='To Date', readonly=True)
    emi_amount = fields.Float(digits=(5, 2),readonly=True)
    emi_payment_date = fields.Date(string='Payment Date')
    invoice_id = fields.Many2one('account.move')
    invoice_id_state = fields.Selection(related='invoice_id.state',store=True,string='Invoice State')
    

    def view_invoice(self):
        invoice_ids = self.invoice_ids
    
        view_ref = self.env['ir.model.data'].get_object_reference('account', 'invoice_form')
        view_id = view_ref[1] if view_ref else False
        res = {
                'type': 'ir.actions.act_window',
                'name': _('Customer Invoice'),
                'res_model': 'account.move',
                'view_mode': 'form',
                'view_id': view_id,
                'res_id' : invoice_ids.id,
                'target': 'current'
               }
    
        return res
    

    def emi_invoice(self):
        invoice_obj =self.env['account.move']
        inv_fields = invoice_obj.fields_get()
        default_value = invoice_obj.default_get(inv_fields)
    
        invoice_line = self.env['account.move.line']
        line_f = invoice_line.fields_get()
        default_line = invoice_line.default_get(line_f)
    
        default_value.update({'partner_id': self.sale_policy_id.policy_holder.id,
                              'currency_id': self.sale_policy_id.branch_name.currency_id.id,
                              'company_id': self.sale_policy_id.branch_name.id,
                              'invoice_date': self.emi_start_date,
                              'invoice_payment_term_id': self.sale_policy_id.policy_term.id,
                              'move_type':'out_invoice',
                              'l10n_in_gst_treatment':'unregistered'
                              })
        invoice = invoice_obj.new(default_value)
        invoice._onchange_partner_id()
        accounts = self.sale_policy_id.policy_schemes.product_name.product_tmpl_id.get_product_accounts(fiscal_pos=False)
        default_value.update({  'invoice_date_due': invoice.invoice_date_due,
                                'invoice_line_ids': [(0, 0,{
                                'product_id': self.sale_policy_id.policy_schemes.product_name.id,
                                'name': self.sale_policy_id.policy_schemes.product_name.name,
                                'price_unit': self.emi_amount,
                                'account_id': accounts['income'].id,
                                'quantity':1,
                                'display_type':False
            })]
             })

        inv_id = invoice.create(default_value)
    
        inv_id.action_invoice_print()
        template_obj = self.env.ref('account.email_template_edi_invoice', False)
        template_obj.send_mail(inv_id.id)
        self.invoice_id=inv_id.id
        return True
    
    @api.model
    def policy_invoice_scheduler(self):
        today_date = datetime.now()
        search_ids = self.env['policy.emi.line'].search(
            [('emi_start_date', '<=', today_date), ('invoice_id', '=', False)])
    
        for i in search_ids:
            i.emi_invoice()
        return True
    
    @api.model
    def create(self, vals):
        return super(policy_emi, self.with_context(mail_create_nolog=True)).create(vals)
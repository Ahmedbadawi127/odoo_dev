# -*- coding: utf-8 -*-
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.fields import Datetime


class LabDoctors(models.Model):
    _name = 'lab.doctors'
    _rec_name = 'combination'

    seq_doc_no = fields.Char(string='Doctor Reference', required=True, copy=False, readonly=True,
                             states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    combination = fields.Char(compute='name_get')
    name = fields.Char()
    address = fields.Char()
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    landline = fields.Char()
    mobile_1 = fields.Char()
    mobile_2 = fields.Char()
    email = fields.Char(string='E-Mail')
    governorate = fields.Many2one('governorate_selection')
    city = fields.Many2one('city_selection')
    age = fields.Integer()
    age_now = fields.Char(compute='age_increase', string='Age', invisible=True)
    count_cases = fields.Integer(compute = '_compute_count_cases')
    # compute = '_compute_count_cases'
    cases_ids = fields.One2many('lab.cases', 'doctor_id')

    total_billing = fields.Integer('Total Billing Funds')
    total_received = fields.Integer('Total Received Funds')
    total_remaining = fields.Integer('Total Remaining Funds', compute='remained_funds')



    # def count(self):
    #     LabCases = self.env['lab.cases']
    #     for rec in self:
    #         # domain = [('partner_id', '=', 'amro')]
    #         domain = [('doctor', '=', 'amro')]
    #         result = LabCases.search(domain)
    #         print(result)

    @api.depends('cases_ids.def_count')
    def _compute_count_cases(self):
        co = 0
        for rec in self:
            for line in rec.cases_ids:
                co += line.def_count
            rec.count_cases = co


    @api.model
    def create(self, vals):
        if vals.get('seq_doc_no', _('New')) == _('New'):
            vals['seq_doc_no'] = self.env['ir.sequence'].next_by_code('lab.doctors.sequence') or _('New')
        result = super(LabDoctors, self).create(vals)
        return result

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, "%s %s %s" % (rec.seq_doc_no, ' | ', rec.name)))
        return res

    #

    @api.depends('age', 'create_date')
    def age_increase(self):
        for rec in self:
            if rec.create_date:
                year_created = datetime.strptime(rec.create_date, '%Y-%m-%d %H:%M:%S').year
                aga = rec.age
                now = Datetime.now()
                year_now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S').year
                year_difference = int(year_now) - int(year_created)
                rec.age_now = str(year_difference + aga)

    @api.onchange('total_billing', 'total_received')
    def remained_funds(self):
        for rec in self:
            rec.total_remaining = rec.total_billing - rec.total_received
    #


class LabCases(models.Model):
    _name = 'lab.cases'
    _rec_name = 'seq_case_no'

    seq_case_no = fields.Char(string='Cases Reference', required=True, copy=False, readonly=True,
                              states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    patient = fields.Char()
    shade = fields.Many2one('shade_selection')
    entry_date = fields.Date(default=fields.Date.today)
    days_processing = fields.Char()
    delivery_date = fields.Date()
    diagnosis_ids = fields.One2many('lab.diagnosis', 'case_id')
    doctor = fields.Many2one('lab.doctors', required=True)
    price = fields.Float(compute='_compute_total_price', string='Total Price')
    discount = fields.Float()
    billed_price = fields.Float(compute='calc_billed_price')
    estimated_cost = fields.Float()
    estimated_profit = fields.Float(compute='calc_estimated_profit')
    userid = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, readonly=True)
    def_count = fields.Integer(default='1', readonly=True)
    doctor_id = fields.Many2one('lab.doctors', select=True, readonly=True)
    state = fields.Selection([
        ('registration', 'Registration'),
        ('bropha', 'Bropha'),
        ('manufacturing', 'Manufacturing'),
        ('delivering', 'Delivering'),
        ('completed', 'Completed')
    ], string='Status', readonly=True, default='registration')

    def action_registered(self):
        for rec in self:
            rec.state = 'bropha'

    def action_confirm_bropha(self):
        for rec in self:
            rec.state = 'manufacturing'

    def action_manufactured(self):
        for rec in self:
            rec.state = 'delivering'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'

    @api.model
    def create(self, vals):
        if vals.get('seq_case_no', _('New')) == _('New'):
            vals['seq_case_no'] = self.env['ir.sequence'].next_by_code('lab.cases.sequence') or _('New')
        result = super(LabCases, self).create(vals)
        return result

    @api.onchange('price', 'discount')
    def calc_billed_price(self):
        for rec in self:
            rec.billed_price = rec.price - (rec.price * (rec.discount / 100))

    @api.onchange('billed_price', 'estimated_cost')
    def calc_estimated_profit(self):
        for rec in self:
            rec.estimated_profit = rec.billed_price - rec.estimated_cost

    @api.onchange('entry_date')
    def _calculate_delivery_date(self):
        if self.entry_date:
            days_added = int(self.days_processing)
            date_1 = (datetime.strptime(self.entry_date, '%Y-%m-%d') + relativedelta(
                days=+ days_added))
            self.delivery_date = date_1
        else:
            self.delivery_date = False

    @api.depends('diagnosis_ids.subtotal_t_p')
    def _compute_total_price(self):
        pr = 0.0
        for rec in self:
            for line in rec.diagnosis_ids:
                pr += line.subtotal_t_p
            rec.price = pr


    def Set_State_Bropha(self):
        self.write({
            'state': 'bropha'
        })

    def Set_State_Manufacturing(self):
        self.write({
            'state': 'manufacturing'
        })

    def Set_State_Delivering(self):
            self.write({
                'state': 'delivering'
            })

    def Set_State_Completed(self):
                self.write({
                    'state': 'completed'
                })





class LabDiagnosis(models.Model):
    _name = 'lab.diagnosis'

    case_id = fields.Many2one('lab.cases', select=True, readonly=True)
    type = fields.Selection([('separated', 'Separated'), ('connected', 'Connected')])
    side = fields.Selection([('upper_left', 'UL'), ('upper_right', 'UR'), ('lower_left', 'LL'), ('lower_right', 'LR')])
    t_1 = fields.Many2one('material_selection')
    t_2 = fields.Many2one('material_selection')
    t_3 = fields.Many2one('material_selection')
    t_4 = fields.Many2one('material_selection')
    t_5 = fields.Many2one('material_selection')
    t_6 = fields.Many2one('material_selection')
    t_7 = fields.Many2one('material_selection')
    t_8 = fields.Many2one('material_selection')

    t_1_p = fields.Float(string='t_1_p', related='t_1.price')
    t_2_p = fields.Float(string='t_1_p', related='t_2.price')
    t_3_p = fields.Float(string='t_1_p', related='t_3.price')
    t_4_p = fields.Float(string='t_1_p', related='t_4.price')
    t_5_p = fields.Float(string='t_1_p', related='t_5.price')
    t_6_p = fields.Float(string='t_1_p', related='t_6.price')
    t_7_p = fields.Float(string='t_1_p', related='t_7.price')
    t_8_p = fields.Float(string='t_1_p', related='t_8.price')
    subtotal_t_p = fields.Float('SubTotal Price', compute='calc_subtotal_price')

    @api.onchange('t_1_p', 't_2_p', 't_3_p', 't_4_p', 't_5_p', 't_6_p', 't_7_p', 't_8_p')
    def calc_subtotal_price(self):
        for rec in self:
            rec.subtotal_t_p = rec.t_1_p + rec.t_2_p + rec.t_3_p + rec.t_4_p + rec.t_5_p + rec.t_6_p + rec.t_7_p + rec.t_8_p


class LabSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_days_processing = fields.Char('Days Till Delivery Date', default_model='lab.cases')

    # default_type1_name = fields.Many2one('material_selection', string='Material', default_model='lab.cases')
    # default_type1_price = fields.Char('Material price', default_model='lab.cases')

    @api.multi
    def set_values(self):
        res = super(LabSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('lab.default_days_processing',
                                                         self.default_days_processing)

        return res

    @api.model
    def get_values(self):
        res = super(LabSettings, self).get_values()

        days_processing_o = self.env['ir.config_parameter'].sudo().get_param(
            'lab.default_days_processing')

        res.update(

            default_days_processing=days_processing_o
        )
        return res
#
#
# class LabTest(models.Model):
#     _name = 'lab.test'
#
#     test = fields.Many2one('lab.cases')
#     test_id = fields.Many2one('lab.doctors')



class LabCasesReportWizard(models.TransientModel):
    _name = 'report.lab.cases.report__cases_dates_wizard'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }



        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        return self.env.ref('cj_custom_report.cases_periodically_report').report_action(self, data=data)


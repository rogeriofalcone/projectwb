# -*- coding: utf-8 -*-
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    wbs_element_id = fields.Many2one(
        comodel_name='project.wbs_element',
        string='WBS Element',
        copy=True
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic account')

    wbs_element_account = fields.Many2one(
        'account.analytic.account',
        string='Wbs Analytic Account')

    @api.onchange('wbs_element_id')
    def _onchange_wbs_element_id(self):
        if self.wbs_element_id:
            self.project_id = self.wbs_element_id.project_id

    @api.multi
    @api.constrains('wbs_element_id')
    def _check_wbs_element_assigned(self):
        for record in self:
            if record.wbs_element_id and record.wbs_element_id.child_ids:
                raise UserError(
                    _('A WBS Element that is parent of others cannot have '
                      'concepts assigned.'))

    @api.model
    def create(self, values):
        task = super(ProjectTask, self).create(values)
        if not task.wbs_element_id:
            name = task.name
        else:
            name = ('[' + task.wbs_element_id.code + '] ' +
                    task.wbs_element_id.name + ' / ' + task.name)
        task.analytic_account_id = (
            task.analytic_account_id.create({
                'company_id': self.env.user.company_id.id,
                'name': name,
                'account_type': 'normal'}))
        task.wbs_element_account = (
            task.wbs_element_id.analytic_account_id)
        return task

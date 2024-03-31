from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit for messaging features

    name = fields.Char('Subject', required=True)
    description = fields.Html('Description')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    customer_email = fields.Char(related='customer_id.email', string='Customer Email')
    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team')
    user_id = fields.Many2one('res.users', string='Assigned To', default=lambda self: self.env.user)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium')

    def create(self, vals_list):
        tickets = super(HelpdeskTicket, self).create(vals_list)
        for ticket in tickets:
            ticket.name = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or 'New Ticket'
        return tickets

class HelpdeskTeam(models.Model):
    _name = 'helpdesk.team'
    _description = 'Helpdesk Team'

    name = fields.Char('Team Name', required=True)

class HelpdeskCategory(models.Model):
    _name = 'helpdesk.category'
    _description = 'Helpdesk Category'

    name = fields.Char('Category Name', required=True)

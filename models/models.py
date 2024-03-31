# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Helpdesk Ticket'

    name = fields.Char('Subject', required=True)
    description = fields.Html('Description')
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    customer_name = fields.Char(related='customer_id.name', string="Customer Name")
    customer_email = fields.Char(related='customer_id.email', string="Customer Email")
    customer_phone = fields.Char(related='customer_id.phone', string="Customer Phone")
    team_id = fields.Many2one('helpdesk.team', string='Helpdesk Team')
    category_id = fields.Many2one('helpdesk.category', string='Helpdesk Category')
    user_id = fields.Many2one('res.users', string='Assigned To', default=lambda self: self.env.user)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='State', default='draft', tracking=True)

    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Attachments'
    )
    active = fields.Boolean(string="Active", default=True)

    def toggle_active(self):
        for ticket in self:
            ticket.active = not ticket.active

    def action_mark_open(self):
        self.state = 'open'

    def action_mark_pending(self):
        self.state = 'pending'

    def action_set_to_draft(self):
        self.state = 'draft'

    def action_mark_resolved(self):
        self.state = 'resolved'

    def action_close_ticket(self):
        self.state = 'closed'
        self.send_ticket_close_email(self)
        # ... (Potentially add actions here: archive ticket, calculate metrics)

    @api.model
    def create(self, vals_list):
        tickets = super(HelpdeskTicket, self).create(vals_list)
        if tickets:
            for ticket in tickets:
                ticket.name = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or 'New Ticket'
            self.send_ticket_creation_email(tickets)
            return tickets

    def send_ticket_creation_email(self, ticket):
        if ticket.customer_email:
            template = self.env.ref('customer_helpdesk.ticket_creation_email_template')
            template.send_mail(ticket.id, force_send=True)

    def send_ticket_close_email(self, ticket):
        if ticket.customer_email:
            template = self.env.ref('customer_helpdesk.ticket_closed_email_template')
            template.send_mail(ticket.id, force_send=True)

    def action_assign_to_me(self):
        self.ensure_one()  # Ensure the function works on a single record
        self.user_id = self.env.user

        # ... inside your HelpdeskTicket model ...




class HelpdeskTeam(models.Model):
    _name = 'helpdesk.team'
    _description = 'Helpdesk Team'

    name = fields.Char('Team Name', required=True)


class HelpdeskCategory(models.Model):
    _name = 'helpdesk.category'
    _description = 'Helpdesk Category'

    name = fields.Char('Category Name', required=True)


# class HelpdeskReportWizard(models.TransientModel):
#     _name = "helpdesk.report.wizard"
#
#     date_from = fields.Date(string="Start Date", required=True)
#     date_to = fields.Date(string="End Date", required=True)
#
#     def get_report_data(self):

#
#     def generate_report(self):
#         data = self.get_report_data()
#         return self.env.ref('customer_helpdesk.action_helpdesk_ticket_report').report_action(self, data=data)

class TicketReportWizard(models.TransientModel):
    _name = 'ticket.report.wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def get_report_data(self):
        tickets = self.env['helpdesk.ticket'].sudo().search([
            ('create_date', '>=', self.start_date),
            ('create_date', '<=', self.end_date)
        ])
        ticket_list = []
        for ticket in tickets:
            ticket_list.append({
                "ticket": ticket.id,
                "subject": ticket.name,
                "customer": ticket.customer_id.name,
                "date": ticket.create_date,
            })
        return {
            'tickets': ticket_list,
            'tickets_count': len(tickets),
            'date_from': self.start_date,
            'date_to': self.end_date,
        }


    def generate_report(self):
        data = self.get_report_data()
        return self.env.ref('customer_helpdesk.action_helpdesk_ticket_report').report_action(self, data=data)


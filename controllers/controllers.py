from odoo import http
from odoo.http import request
import base64


class HelpdeskFormController(http.Controller):
    @http.route('/helpdesk/submit_ticket', type='http', auth="public", website=True)
    def submit_helpdesk_ticket(self, **kw):
        if request.httprequest.method == 'POST':
            # Create customer (contact)
            partner_vals = {
                'name': kw.get('customer_name'),
                'email': kw.get('customer_email'),
                'phone': kw.get('customer_phone'),
            }
            new_partner = request.env['res.partner'].sudo().create(partner_vals)

            if new_partner:
                attachments = self._handle_attachments(request.httprequest.files.getlist('attachments'))
                ticket_vals = {
                    'name': kw.get('subject'),
                    'description': kw.get('description'),
                    'customer_id': new_partner.id,  # Link the customer
                    'team_id': int(kw.get('team_id')),
                    'category_id': int(kw.get('category_id')),
                    'priority': kw.get('priority'),
                    'attachment_ids': attachments,  # Update attachment_ids
                }
                new_ticket = request.env['helpdesk.ticket'].sudo().create(ticket_vals)
                return request.render("customer_helpdesk.ticket_submission_success", {'ticket': new_ticket})

            # Fetch teams and categories for the form
        teams = request.env['helpdesk.team'].sudo().search([])
        categories = request.env['helpdesk.category'].sudo().search([])
        return request.render("customer_helpdesk.helpdesk_form", {
            'teams': teams,
            'categories': categories
        })

    def _handle_attachments(self, files):
        attachments = []
        for file in files:
            attachment_value = {
                'name': file.filename,
                'res_name': file.filename,
                'datas': base64.encodestring(file.read()),
                'type': 'binary',
                'res_model': 'helpdesk.ticket',
                'res_field': 'attachment_ids',
            }
            attachments.append((0, 0, attachment_value))
        return attachments

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class SadadController(http.Controller):

    @http.route(['/payment/sadad/return'], type='http', auth='public', csrf=False)
    def sadad_return(self, **post):
        _logger.info('Sadad: entering form_feedback with post data %s', post)
        request.env['payment.transaction'].sudo().form_feedback(post, 'sadad')
        return request.redirect('/payment/status')

    @http.route(['/payment/sadad/cancel'], type='http', auth='public', csrf=False)
    def sadad_cancel(self, **post):
        _logger.info('Sadad: payment cancelled with post data %s', post)
        return request.redirect('/payment/status')

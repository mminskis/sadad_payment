import json
import logging
import requests
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class PaymentProviderSadad(models.Model):
    _inherit = 'payment.provider'  # Changed from payment.acquirer to payment.provider

    # Use selection_add to dynamically add 'Sadad' to the existing providers without removing the others
    provider = fields.Selection(selection_add=[('sadad', 'Sadad')])

    sadad_merchant_id = fields.Char(
        'Sadad Merchant ID', required_if_provider='sadad', groups='base.group_user')
    sadad_secret_key = fields.Char(
        'Sadad Secret Key', required_if_provider='sadad', groups='base.group_user')

    def _get_sadad_urls(self):
        """ Sadad URLS """
        return {
            'sadad_form_url': 'https://api.sadad.qa/payment',
        }

    def sadad_form_generate_values(self, values):
        self.ensure_one()
        sadad_tx_values = dict(values)
        sadad_tx_values.update({
            'merchant_id': self.sadad_merchant_id,
            'secret_key': self.sadad_secret_key,
            'amount': values['amount'],
            'currency': values['currency'] and values['currency'].name or '',
            'order_id': values['reference'],
            'description': 'Payment for order %s' % values['reference'],
            'callback_url': self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/payment/sadad/return',
            'cancel_url': self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/payment/sadad/cancel',
        })
        return sadad_tx_values

    def sadad_get_form_action_url(self):
        self.ensure_one()
        return self._get_sadad_urls()['sadad_form_url']


class PaymentTransactionSadad(models.Model):
    _inherit = 'payment.transaction'

    sadad_txn_id = fields.Char(string='Sadad Transaction ID')

    def _sadad_form_get_tx_from_data(self, data):
        reference = data.get('order_id')
        txn = self.search([('reference', '=', reference)])
        if not txn or len(txn) > 1:
            error_msg = 'Sadad: received data for reference %s; no order found' % reference
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return txn

    def _sadad_form_validate(self, data):
        self.ensure_one()
        if data.get('status') == 'SUCCESS':
            self._set_transaction_done()
            return True
        else:
            self._set_transaction_error('Sadad: feedback error')
            return False

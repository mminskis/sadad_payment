import json
import logging
import requests
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentProviderSadad(models.Model):
    _inherit = 'payment.provider'

    # Adding 'sadad' to the selection field for code, with an ondelete policy
    code = fields.Selection(
        selection_add=[('sadad', 'Sadad')], ondelete={'sadad': 'cascade'})

    # Fields for Sadad credentials
    sadad_merchant_id = fields.Char(
        'Sadad Merchant ID', groups='base.group_user')
    sadad_secret_key = fields.Char(
        'Sadad Secret Key', groups='base.group_user')

    def _get_sadad_urls(self):
        """ Return Sadad's payment gateway URLs """
        return {
            'sadad_form_url': 'https://api.sadad.qa/payment',
        }

    def sadad_form_generate_values(self, values):
        """ Generate the values for the Sadad payment form """
        self.ensure_one()

        # Ensure merchant ID and secret key are set for Sadad before proceeding
        if not self.sadad_merchant_id or not self.sadad_secret_key:
            raise ValidationError(
                "Sadad Merchant ID and Secret Key must be set for Sadad payment provider.")

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
        """ Return the Sadad form action URL """
        self.ensure_one()
        return self._get_sadad_urls()['sadad_form_url']

    @api.constrains('sadad_merchant_id', 'sadad_secret_key')
    def _check_sadad_credentials(self):
        """ Ensure that the credentials are not empty when the Sadad provider is used """
        for provider in self:
            if provider.code == 'sadad' and (not provider.sadad_merchant_id or not provider.sadad_secret_key):
                raise ValidationError(
                    "Sadad Merchant ID and Secret Key are required for Sadad payment provider.")

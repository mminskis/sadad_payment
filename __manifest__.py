{
    'name': 'Sadad Payment Gateway',
    'version': '1.0',
    'category': 'Payment',
    'summary': 'Integration with Sadad Payment Gateway for Odoo',
    'description': """This module integrates Sadad payment gateway with Odoo eCommerce, supporting Apple Pay and card payments.""",
    'author': 'Your Name',
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/payment_template.xml',
        'data/payment_provider_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#import json
#import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale
import re
from odoo import fields, tools, _



class NsWebsiteSaleForm(WebsiteSale):


    def checkout_form_validate(self, mode, all_form_values, data):
        res=super(NsWebsiteSaleForm, self).checkout_form_validate(mode, all_form_values, data)
        error={}
        error_message=[]
        if data.get('phone'):
            if len(data.get('phone')) > 10:
            # if len(data.get('phone')) <5 or len(data.get('phone'))>10:
                 error['phone'] = 'error'
                 error_message.append(_(
                     "Please Check phone number. it cant be more than 10 numbers."
                 ))
                 return (error,error_message)
            pattern = re.compile("69[0-9]{8}")
            if not pattern.match(data.get('phone')):
                error['phone'] = 'error'
                error_message.append(_(
                    "Please check phone number format. it cant be less than 10 numbers."
                ))
                return (error,error_message)
        


        if data.get('zip'):
            if len(data.get('zip')) > 5:
            # if len(data.get('phone')) <5 or len(data.get('phone'))>10:
                 error['zip'] = 'error'
                 error_message.append(_(
                     "Please Check zip. it cant be more than 5 numbers."
                 ))
                 return (error,error_message)
            pattern = re.compile("[0-9]{5}")
            if not pattern.match(data.get('zip')):
                error['zip'] = 'error'
                error_message.append(_(
                    "Please check zip format. it can't be less than 5 numbers."
                ))
                return (error,error_message)

        return res

    # the original function follows.

    def checkout_form_validate(self, mode, all_form_values, data):
        # mode: tuple ('new|edit', 'billing|shipping')
        # all_form_values: all values before preprocess
        # data: values after preprocess
        error = dict()
        error_message = []

        if data.get('partner_id'):
            partner_su = request.env['res.partner'].sudo().browse(int(data['partner_id'])).exists()
            name_change = partner_su and 'name' in data and data['name'] != partner_su.name
            email_change = partner_su and 'email' in data and data['email'] != partner_su.email

            # Prevent changing the partner name if invoices have been issued.
            if name_change and not partner_su.can_edit_vat():
                error['name'] = 'error'
                error_message.append(_(
                    "Changing your name is not allowed once invoices have been issued for your"
                    " account. Please contact us directly for this operation."
                ))

            # Prevent change the partner name or email if it is an internal user.
            if (name_change or email_change) and not all(partner_su.user_ids.mapped('share')):
                error.update({
                    'name': 'error' if name_change else None,
                    'email': 'error' if email_change else None,
                })
                error_message.append(_(
                    "If you are ordering for an external person, please place your order via the"
                    " backend. If you wish to change your name or email address, please do so in"
                    " the account settings or contact your administrator."
                ))

        # Required fields from form
        required_fields = [f for f in (all_form_values.get('field_required') or '').split(',') if f]

        # Required fields from mandatory field function
        country_id = int(data.get('country_id', False))
        required_fields += mode[1] == 'shipping' and self._get_mandatory_fields_shipping(country_id) or self._get_mandatory_fields_billing(country_id)

        # error message for empty required fields
        for field_name in required_fields:
            val = data.get(field_name)
            if isinstance(val, str):
                val = val.strip()
            if not val:
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        Partner = request.env['res.partner']
        if data.get("vat") and hasattr(Partner, "check_vat"):
            if country_id:
                data["vat"] = Partner.fix_eu_vat_number(country_id, data.get("vat"))
            partner_dummy = Partner.new(self._get_vat_validation_fields(data))
            try:
                partner_dummy.check_vat()
            except ValidationError as exception:
                error["vat"] = 'error'
                error_message.append(exception.args[0])

        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message
    

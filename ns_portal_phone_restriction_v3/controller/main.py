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
    

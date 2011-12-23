import urllib, math

from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter

from Products.CMFCore.utils import getToolByName

from pcommerce.core.interfaces import IPaymentMethod
from pcommerce.core.currency import CurrencyAware
from pcommerce.core import PCommerceMessageFactory as _

from pcommerce.payment.saferpay.interfaces import ISaferpayPayment

class SaferpayPayment(object):
    implements(IPaymentMethod, ISaferpayPayment)
    adapts(Interface)
    
    title = _(u'Saferpay')
    description = _('Payment using Saferpay')
    icon = u'++resource++pcommerce_payment_saferpay_icon.gif'
    logo = u'++resource++pcommerce_payment_saferpay_logo.gif'
    
    def __init__(self, context):
        self.context = context
        self.props = getToolByName(self.context, 'portal_properties').saferpay_properties
        
    def __getattr__(self, name):
        if self.props.hasProperty(name):
            return self.props.getProperty(name)
        raise AttributeError
    
    def mailInfo(self, order, lang=None, customer=False):
        return _('saferpay_mailinfo', default=u"Payment processed over Saferpay")

    def verifyPayment(self, order):
        """"""
        # TODO: server certificate verification (M2Crypto)
        url = 'https://www.saferpay.com/hosting/VerifyPayConfirm.asp'
        params = {'SIGNATURE': self.context.REQUEST.get('SIGNATURE', None),
                  'DATA': self.context.REQUEST.get('DATA', None)}
        data = urllib.urlopen(url, urllib.urlencode(params)).read()
        if data.startswith('OK'):
            url = 'https://www.saferpay.com/hosting/PayComplete.asp'
            params = {'ACCOUNTID': self.account_id,
                      'ID': data[6:data.find('&')]}
            if self.test:
                params.update({'spPassword': self.password})
            data = urllib.urlopen(url, urllib.urlencode(params))
            return True
        return False
        
    def action(self, order):
        """"""
        # TODO: server certificate verification (M2Crypto)
        url = '%s/%%s' % (self.context.absolute_url())
        props = getToolByName(self.context, 'portal_properties').pcommerce_properties
        portal_state = getMultiAdapter((self.context, self.context.REQUEST), name=u'plone_portal_state')
        lang = self.context.REQUEST.get('LANGUAGE', portal_state.default_language())
        price = CurrencyAware(order.totalincl)
        params = {'AMOUNT': int(math.ceil(price.getRoundedValue() * 100)),
                  'CURRENCY': order.currency.upper() or 'EUR',
                  'DESCRIPTION': props.getProperty('productname', portal_state.portal().getProperty('title', '')),
                  'SUCCESSLINK': url % 'payment.success',
                  'FAILLINK': url % 'payment.failed',
                  'BACKLINK': url % 'payment.cancel',
                  'NOTIFYURL': '%s/processSaferpay?%s' % (portal_state.portal_url(), lang),
                  'NOTIFYADDRESS': portal_state.portal().getProperty('email_from_address', ''),
                  'USERNOTIFY': portal_state.member().getProperty('email', ''),
                  'LANGID': lang[:2].lower(),
                  'ALLOWCOLLECT': 'no',
                  'DELIVERY': 'no',
                  'ACCOUNTID': self.account_id,
                  'ORDERID': order.orderid,
                  'BODYCOLOR': self.bodycolor,
                  'HEADCOLOR': self.headcolor,
                  'HEADLINECOLOR': self.headlinecolor,
                  'MENUCOLOR': self.menucolor,
                  'BODYFONTCOLOR': self.bodyfontcolor,
                  'HEADFONTCOLOR': self.headfontcolor,
                  'MENUFONTCOLOR': self.menufontcolor,
                  'FONT': self.font}
        url = 'https://www.saferpay.com/hosting/CreatePayInit.asp'
        data = urllib.urlopen(url, urllib.urlencode(params))
        return data.read()

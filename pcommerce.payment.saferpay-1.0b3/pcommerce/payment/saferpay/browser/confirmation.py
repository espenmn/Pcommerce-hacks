from zope.interface import implements
from zope.i18n import translate

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pcommerce.core.interfaces import IPaymentView
from pcommerce.core import PCommerceMessageFactory as _

class SaferpayConfirmation(BrowserView):
    template = ViewPageTemplateFile('confirmation.pt')
    implements(IPaymentView)
    
    def __init__(self, payment, request):
        self.payment = payment
        self.context = payment.context
        self.request = request
    
    def __call__(self):
        return self.template()

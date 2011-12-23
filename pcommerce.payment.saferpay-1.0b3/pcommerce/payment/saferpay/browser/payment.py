from zope.interface import implements

from Products.Five.browser import BrowserView

from pcommerce.core.interfaces import IPaymentView

from pcommerce.payment.saferpay.data import SaferpayPaymentData

class SaferpayPayment(BrowserView):
    implements(IPaymentView)
    
    def __init__(self, payment, request):
        self.payment = payment
        self.context = payment.context
        self.request = request
    
    def validate(self):
        return True
    
    def process(self):
        return SaferpayPaymentData()
    
    def renders(self):
        return False

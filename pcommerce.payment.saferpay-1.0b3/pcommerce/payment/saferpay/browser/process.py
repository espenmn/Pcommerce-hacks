from xml.dom import minidom

from Products.Five.browser import BrowserView

from pcommerce.core.interfaces import IPaymentProcessor

class ProcessSaferpay(BrowserView):
    """process Saferpay payments
    """

    def __call__(self):
        lang = self.request.get('QUERY_STRING', None)
        if not lang:
            lang = None
        processor = IPaymentProcessor(self.context)
        data = minidom.parseString(self.request.get('DATA', ''))
        return processor.processOrder(data.firstChild.getAttribute('ORDERID'), 'pcommerce.payment.saferpay', lang)

from Acquisition import aq_inner

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone import PloneMessageFactory as _p
from pcommerce.payment.saferpay import config


class Configlet(BrowserView):
    """Saferpay configlet
    """

    errors = {}
    values = {}
    template = ViewPageTemplateFile('configlet.pt')
    properties = [k.get('name') for k in config.CONFIGLET_PROPERTIES]
    required = [k.get('name') for k in config.CONFIGLET_PROPERTIES if k.get('required')]

    def __call__(self):

        self.request.set('disable_border', True)

        if self.request.form.has_key('saferpay_save'):
            self.setProperties()

        props = getToolByName(self.context, 'portal_properties').saferpay_properties
        for property in self.properties:
            self.values[property] = props.getProperty(property, '')

        return self.template()

    def setProperties(self):
        context = aq_inner(self.context)
        utils = getToolByName(context, 'plone_utils')
        self.errors = {}
        for prop in self.properties:
            self.values[prop] = self.request.form.get(prop, None)
            if self.values[prop] == '':
                self.values[prop] = None
            if prop in self.required and self.values[prop] is None:
                self.errors[prop] = _p(u'This field is required')
        if len(self.errors) > 0:
            utils.addPortalMessage(_p(u'Please correct the indicated errors'))
        else:
            props = getToolByName(context, 'portal_properties').saferpay_properties
            for property in self.properties:
                props._setPropValue(property, self.values[property])
            utils.addPortalMessage(_p(u'Properties saved'))

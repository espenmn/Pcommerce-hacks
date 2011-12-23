from Products.CMFCore.utils import getToolByName
from pcommerce.payment.saferpay import config

# Properties are defined here, because if they are defined in propertiestool.xml,
# all properties are re-set the their initial state if you reinstall product
# in the quickinstaller.

SAFERPAY = 'saferpay_properties'

def setupVarious(context):

    if not context.readDataFile('pcommerce.payment.saferpay_various.txt'):
        return
    portal = context.getSite()
    
    portal_properties = getToolByName(portal, 'portal_properties')
    
    if not SAFERPAY in portal_properties:
        portal_properties.manage_addPropertySheet(SAFERPAY)
        
    props = portal_properties.get(SAFERPAY)
    for prop in config.CONFIGLET_PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'], prop['type_'])
    
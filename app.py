import os
import datetime
import bottlenose
import xml.etree.ElementTree as ET

amazonPublicKey = os.environ.get('AmznPublicKey')
amazonSecretKey = os.environ.get('AmznSecretKey')
amazonAssociateID = os.environ.get('AmznAssociateId')
timestamp = datetime.datetime.utcnow()
amzdate = timestamp.strftime('%Y%m%dT%H%M%SZ')
datestamp = timestamp.strftime('%Y%m%d')

amazon = bottlenose.Amazon(amazonPublicKey, amazonSecretKey, amazonAssociateID)


class book(object):

    def __init__(self, ItemID='9780134475585'):  # '9781101873724'):
        self.ItemID = ItemID
        self.NameSpace = {'ns0': 'http://webservices.amazon.com/AWSECommerceService/2013-08-01'}
        self.IdType = 'ISBN'
        self.SearchIndex = 'Books'
        self.ResponseGroup = 'OfferFull'
        self.XMLResponse = amazon.ItemLookup(ItemId=self.ItemID,
                                             IdType=self.IdType,
                                             SearchIndex=self.SearchIndex,
                                             ResponseGroup=self.ResponseGroup)
        self.root = ET.fromstring(self.XMLResponse)
        self.TotalNewOffers = self.root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalNew',
                                                namespaces=self.NameSpace)[0].text
        self.TotalUsedOffers = self.root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalUsed',
                                                 namespaces=self.NameSpace)[0].text
        self.LowestNewPrice = self.root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestNewPrice/ns0:Amount',
                                                namespaces=self.NameSpace)[0].text
        self.LowestUsedPrice = self.root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestUsedPrice/ns0:Amount',
                                                 namespaces=self.NameSpace)[0].text
        self.BuyBoxMerchant = self.root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:Merchant/ns0:Name',
                                                namespaces=self.NameSpace)[0].text


test = book()

print(test.BuyBoxMerchant)

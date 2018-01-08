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

    def __init__(self, ItemID='0134475585'):#'9780134475585'):  # '9781101873724'):
        self.ItemID = ItemID
        self.NameSpace = {'ns0': 'http://webservices.amazon.com/AWSECommerceService/2013-08-01'}
        self.IdType = 'ISBN'
        self.SearchIndex = 'Books'
        self.OfferResponseGroup = 'OfferFull'

        ' Creates element tree for getting offer information for the item'
        self.OfferXMLResponse = amazon.ItemLookup(ItemId=self.ItemID,
                                             IdType=self.IdType,
                                             SearchIndex=self.SearchIndex,
                                             ResponseGroup=self.OfferResponseGroup)
        self.OfferRoot = ET.fromstring(self.OfferXMLResponse)

        ' Creates element tree for getting sales rank/ASIN of the item'
        self.RankXMLResponse = amazon.ItemLookup(ItemId=self.ItemID,
                                                  IdType=self.IdType,
                                                  SearchIndex=self.SearchIndex,
                                                  ResponseGroup='SalesRank')
        self.RankRoot = ET.fromstring(self.RankXMLResponse)

        ' Creates element tree for getting item attributes'
        self.ItemXMLResponse = amazon.ItemLookup(ItemId=self.ItemID,
                                                 IdType=self.IdType,
                                                 SearchIndex=self.SearchIndex,
                                                 ResponseGroup='ItemAttributes')
        self.ItemRoot = ET.fromstring(self.ItemXMLResponse)

        ' Creates element tree for getting item images'
        self.ImageXMLResponse = amazon.ItemLookup(ItemId=self.ItemID,
                                                 IdType=self.IdType,
                                                 SearchIndex=self.SearchIndex,
                                                 ResponseGroup='Images')
        self.ImageRoot = ET.fromstring(self.ImageXMLResponse)

        self.TotalNewOffers = self.OfferRoot.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalNew',
                                                     namespaces=self.NameSpace)[0].text
        self.TotalUsedOffers = self.OfferRoot.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalUsed',
                                                      namespaces=self.NameSpace)[0].text
        self.LowestNewPrice = self.OfferRoot.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestNewPrice/ns0:Amount',
                                                     namespaces=self.NameSpace)[0].text
        self.LowestUsedPrice = self.OfferRoot.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestUsedPrice/ns0:Amount',
                                                      namespaces=self.NameSpace)[0].text
        self.BuyBoxMerchant = self.OfferRoot.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:Merchant/ns0:Name',
                                                     namespaces=self.NameSpace)[0].text
        self.ASIN = self.RankRoot.findall('ns0:Items/ns0:Item/ns0:ASIN', namespaces=self.NameSpace)[0].text
        self.SalesRank = self.RankRoot.findall('ns0:Items/ns0:Item/ns0:SalesRank', namespaces=self.NameSpace)[0].text
        self.Author = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Author', namespaces=self.NameSpace)[0].text
        self.BookBinding = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Binding', namespaces=self.NameSpace)[0].text
        self.Publisher = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Publisher', namespaces=self.NameSpace)[0].text
        self.Pages = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:NumberOfPages', namespaces=self.NameSpace)[0].text
        self.PublicationDate = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:PublicationDate', namespaces=self.NameSpace)[0].text
        self.ListPrice = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ListPrice/ns0:Amount', namespaces=self.NameSpace)[0].text
        # self.Weight = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Weight', namespaces=self.NameSpace)[0].text
        self.Height = int(self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Height', namespaces=self.NameSpace)[0].text) / 100.0
        self.Length = int(self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Length', namespaces=self.NameSpace)[0].text) / 100.0
        self.Width = int(self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Width', namespaces=self.NameSpace)[0].text) / 100.0
        self.Title = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Title', namespaces=self.NameSpace)[0].text
        self.AmazonTradeValue = self.ItemRoot.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:TradeInValue/ns0:Amount', namespaces=self.NameSpace)[0].text
        self.SmallImageURL = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:URL', namespaces=self.NameSpace)[0].text
        self.SmallImageHeight = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:Height', namespaces=self.NameSpace)[0].text
        self.SmallImageWidth = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:Width', namespaces=self.NameSpace)[0].text
        self.MediumImageURL = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:URL', namespaces=self.NameSpace)[0].text
        self.MediumImageHeight = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:Height', namespaces=self.NameSpace)[0].text
        self.MediumImageWidth = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:Width', namespaces=self.NameSpace)[0].text
        self.LargeImageURL = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:URL', namespaces=self.NameSpace)[0].text
        self.LargeImageHeight = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:Height', namespaces=self.NameSpace)[0].text
        self.LargeImageWidth = self.ImageRoot.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:Width', namespaces=self.NameSpace)[0].text

test = book()

print(test.LargeImageWidth)

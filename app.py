import os
import datetime
import bottlenose
import xml.etree.ElementTree as ET
import mws

amazonPublicKey = os.environ.get('AmznPublicKey')
amazonSecretKey = os.environ.get('AmznSecretKey')
amazonAssociateID = os.environ.get('AmznAssociateId')
MWSAccessKey = os.environ.get('AmznMWSPublicKey')
MWSSecretKey = os.environ.get('AmznMWSSecretKey')
MWSAccountID = os.environ.get('AmznMWSDeveloperID')

timestamp = datetime.datetime.utcnow()
amzdate = timestamp.strftime('%Y%m%dT%H%M%SZ')
datestamp = timestamp.strftime('%Y%m%d')

amazon = bottlenose.Amazon(amazonPublicKey, amazonSecretKey, amazonAssociateID)


# orders_api = mws.Orders(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
# service_status = orders_api.get_service_status()
# service_status

def get_XML_response(isbn, group):
    try:
        return amazon.ItemLookup(ItemId=isbn,
                                 SearchIndex='Books',
                                 IdType='ISBN',
                                 ResponseGroup=group)
    except Exception as e:
        print('Caught exception ' + e + ' in get_XML_response()')


def create_root(xml):
    try:
        return ET.fromstring(xml)
    except Exception as e:
        print('Caught exception ' + e + ' in create_root()')


def get_total_new_offers(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalNew', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_total_new_offers()')


def get_total_used_offers(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalUsed',namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_total_used_offers()')


def get_lowest_new_price(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestNewPrice/ns0:Amount', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_lowest_new_price()')


def get_lowest_used_price(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestUsedPrice/ns0:Amount', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_lowest_used_price()')


def get_buy_box_merchant(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:Merchant/ns0:Name', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_buy_box_merchant()')


def get_asin(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ASIN', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_asin()')


def get_sales_rank(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:SalesRank', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_sales_rank()')


def get_author(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Author', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_author()')


def get_book_binding(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Binding', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_book_binding()')


def get_publisher(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Publisher', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_publisher()')


def get_pages(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:NumberOfPages', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_pages()')


def get_publication_date(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:PublicationDate', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_publication_date()')


def get_list_price(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ListPrice/ns0:Amount', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_list_price()')


def get_weight(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Weight', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_weight()')


def get_height(root, namespace):
    try:
        return int(root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Height', namespaces=namespace)[0].text) / 100.0
    except Exception as e:
        print('Caught exception ' + e + ' in get_height()')


def get_length(root, namespace):
    try:
        return int(root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Length', namespaces=namespace)[0].text) / 100.0
    except Exception as e:
        print('Caught exception ' + e + ' in get_length()')


def get_width(root, namespace):
    try:
        return int(root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Width', namespaces=namespace)[0].text) / 100.0
    except Exception as e:
        print('Caught exception ' + e + ' in get_width()')


def get_title(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Title', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_title()')


def get_amazon_trade_value(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:TradeInValue/ns0:Amount', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_amazon_trade_value()')


def get_small_image_url(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:URL', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_small_image_url()')


def get_small_image_height(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:Height', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_small_image_height()')


def get_small_image_width(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:Width', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_small_image_width()')


def get_medium_image_url(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:URL', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_medium_image_url()')


def get_medium_image_height(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:Height', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_medium_image_height()')


def get_medium_image_width(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:Width', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_medium_image_width()')


def get_large_image_url(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:URL', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_large_image_url()')


def get_large_image_height(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:Height', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_large_image_height()')


def get_large_image_width(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:Width', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_large_image_width()')


class bookers(object):
    def __init__(self, isbn):
        self.Isbn = isbn
        self.NameSpace = {'ns0': 'http://webservices.amazon.com/AWSECommerceService/2013-08-01'}
        self.OfferXMLResponse = get_XML_response(isbn=self.Isbn, group='OfferFull')
        self.OfferRoot = create_root(xml=self.OfferXMLResponse)
        self.RankXMLResponse = get_XML_response(isbn=self.Isbn, group='SalesRank')
        self.RankRoot = create_root(xml=self.RankXMLResponse)
        self.ItemXMLResponse = get_XML_response(isbn=self.Isbn, group='ItemAttributes')
        self.ItemRoot = create_root(xml=self.ItemXMLResponse)
        self.ImageXMLResponse = get_XML_response(isbn=self.Isbn, group='Images')
        self.ImageRoot = create_root(xml=self.ImageXMLResponse)

        self.TotalNewOffers = get_total_new_offers(root=self.OfferRoot, namespace=self.NameSpace)
        self.TotalUsedOffers = get_total_used_offers(root=self.OfferRoot, namespace=self.NameSpace)
        self.LowestNewPrice = get_lowest_new_price(root=self.OfferRoot, namespace=self.NameSpace)
        self.LowestUsedPrice = get_lowest_used_price(root=self.OfferRoot, namespace=self.NameSpace)
        self.BuyBoxMerchant = get_buy_box_merchant(root=self.OfferRoot, namespace=self.NameSpace)
        self.ASIN = get_asin(root=self.RankRoot, namespace=self.NameSpace)
        self.SalesRank = get_sales_rank(root=self.RankRoot, namespace=self.NameSpace)
        self.Author = get_author(root=self.ItemRoot, namespace=self.NameSpace)
        self.BookBinding = get_book_binding(root=self.ItemRoot, namespace=self.NameSpace)
        self.Publisher = get_publisher(root=self.ItemRoot, namespace=self.NameSpace)
        self.Pages = get_pages(root=self.ItemRoot, namespace=self.NameSpace)
        self.PublicationDate = get_publication_date(root=self.ItemRoot, namespace=self.NameSpace)
        self.ListPrice = get_list_price(root=self.ItemRoot, namespace=self.NameSpace)
        # self.Weight = get_weight(root=self.ItemRoot, namespace=self.NameSpace)
        self.Height = get_height(root=self.ItemRoot, namespace=self.NameSpace)
        self.Length = get_length(root=self.ItemRoot, namespace=self.NameSpace)
        self.Width = get_width(root=self.ItemRoot, namespace=self.NameSpace)
        self.Title = get_title(root=self.ItemRoot, namespace=self.NameSpace)
        self.TradeInValue = get_amazon_trade_value(root=self.ItemRoot, namespace=self.NameSpace)
        self.SmallImageUrl = get_small_image_url(root=self.ImageRoot, namespace=self.NameSpace)
        self.SmallImageHeight = get_small_image_height(root=self.ImageRoot, namespace=self.NameSpace)
        self.SmallImageWidth = get_small_image_width(root=self.ImageRoot, namespace=self.NameSpace)
        self.MediumImageUrl = get_medium_image_url(root=self.ImageRoot, namespace=self.NameSpace)
        self.MediumImageHeight = get_medium_image_height(root=self.ImageRoot, namespace=self.NameSpace)
        self.MediumImageWidth = get_medium_image_width(root=self.ImageRoot, namespace=self.NameSpace)
        self.LargeImageUrl = get_large_image_url(root=self.ImageRoot, namespace=self.NameSpace)
        self.LargeImageHeight = get_large_image_height(root=self.ImageRoot, namespace=self.NameSpace)
        self.LargeImageWidth = get_large_image_width(root=self.ImageRoot, namespace=self.NameSpace)


book = bookers('0134475585')

print(book.LargeImageUrl)









# ='0134475585'):#'9780134475585'):  # '9781101873724'):

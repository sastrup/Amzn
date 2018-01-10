import os
import datetime
import bottlenose
import mws
import xml.etree.ElementTree as ET
import statistics as stat
import math

amazonPublicKey = os.environ.get('AmznPublicKey')
amazonSecretKey = os.environ.get('AmznSecretKey')
amazonAssociateID = os.environ.get('AmznAssociateId')
MWSAccessKey = os.environ.get('AmznMWSPublicKey')
MWSSecretKey = os.environ.get('AmznMWSSecretKey')
MWSAccountID = os.environ.get('AmznMWSSellerID')

timestamp = datetime.datetime.utcnow()
amzdate = timestamp.strftime('%Y%m%dT%H%M%SZ')
datestamp = timestamp.strftime('%Y%m%d')

amazon = bottlenose.Amazon(amazonPublicKey, amazonSecretKey, amazonAssociateID)


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
        return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalUsed', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_total_used_offers()')


def get_lowest_new_price(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestNewPrice/ns0:Amount', namespaces=namespace)[
            0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_lowest_new_price()')


def get_lowest_used_price(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestUsedPrice/ns0:Amount', namespaces=namespace)[
            0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_lowest_used_price()')


def get_buy_box_merchant(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:Merchant/ns0:Name', namespaces=namespace)[
            0].text
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
        return float(
            root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:NumberOfPages', namespaces=namespace)[0].text)
    except Exception as e:
        print('Caught exception ' + e + ' in get_pages()')


def get_publication_date(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:PublicationDate', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_publication_date()')


def get_list_price(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ListPrice/ns0:Amount', namespaces=namespace)[
            0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_list_price()')


def get_weight(root, namespace):
    try:
        return \
            root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Weight', namespaces=namespace)[
                0].text / 100.0
    except Exception as e:
        100.0


def get_height(root, namespace):
    try:
        return int(
            root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Height', namespaces=namespace)[
                0].text) / 100.0
    except Exception as e:
        print('Caught exception ' + e + ' in get_height()')


def get_length(root, namespace):
    try:
        return int(
            root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Length', namespaces=namespace)[
                0].text) / 100.0
    except Exception as e:
        print('Caught exception ' + e + ' in get_length()')


def get_width(root, namespace):
    try:
        return int(
            root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Width', namespaces=namespace)[
                0].text) / 100.0
    except Exception as e:
        print('Caught exception ' + e + ' in get_width()')


def get_title(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Title', namespaces=namespace)[0].text
    except Exception as e:
        print('Caught exception ' + e + ' in get_title()')


def get_amazon_trade_value(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:TradeInValue/ns0:Amount', namespaces=namespace)[
            0].text
    except Exception as e:
        return 0


def get_amazon_trade_status(root, namespace):
    try:
        return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:IsEligibleForTradeIn', namespaces=namespace)[
            0].text
    except Exception as e:
        return 0


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


def get_longest_side(sides):
    return max(sides)


def get_shortest_side(sides):
    return min(sides)


def get_median_side(sides):
    return stat.median(sides)


def get_length_girth_number(sides):
    return sum(sides)


def get_shipped_weight(root, namespace):
    try:
        return float(root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:PackageDimensions/ns0:Weight',
                                  namespaces=namespace)[0].text) / 100.0
    except Exception as e:
        print('Caught exception ' + e + ' in get_shipped_weight()')


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
        # self.TotalUsedOffers = get_total_used_offers(root=self.OfferRoot, namespace=self.NameSpace)
        self.LowestNewPrice = get_lowest_new_price(root=self.OfferRoot, namespace=self.NameSpace)
        # self.LowestUsedPrice = get_lowest_used_price(root=self.OfferRoot, namespace=self.NameSpace)
        self.BuyBoxMerchant = get_buy_box_merchant(root=self.OfferRoot, namespace=self.NameSpace)
        self.ASIN = get_asin(root=self.RankRoot, namespace=self.NameSpace)
        self.SalesRank = get_sales_rank(root=self.RankRoot, namespace=self.NameSpace)
        self.Author = get_author(root=self.ItemRoot, namespace=self.NameSpace)
        self.BookBinding = get_book_binding(root=self.ItemRoot, namespace=self.NameSpace)
        self.Publisher = get_publisher(root=self.ItemRoot, namespace=self.NameSpace)
        self.Pages = get_pages(root=self.ItemRoot, namespace=self.NameSpace)
        self.PublicationDate = get_publication_date(root=self.ItemRoot, namespace=self.NameSpace)
        self.ListPrice = get_list_price(root=self.ItemRoot, namespace=self.NameSpace)
        self.Weight = get_weight(root=self.ItemRoot, namespace=self.NameSpace)
        self.Height = get_height(root=self.ItemRoot, namespace=self.NameSpace)
        self.Length = get_length(root=self.ItemRoot, namespace=self.NameSpace)
        self.Width = get_width(root=self.ItemRoot, namespace=self.NameSpace)
        self.Title = get_title(root=self.ItemRoot, namespace=self.NameSpace)
        self.ShippedWeightLbs = get_shipped_weight(root=self.ItemRoot, namespace=self.NameSpace)
        self.ShippedWeightOz = get_shipped_weight(root=self.ItemRoot, namespace=self.NameSpace) * 16.0
        self.TradeInStatus = get_amazon_trade_status(root=self.ItemRoot, namespace=self.NameSpace)
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
        self.LongestSide = get_longest_side([self.Length, self.Height, self.Width])
        self.ShortestSide = get_shortest_side([self.Length, self.Height, self.Width])
        self.MedianSide = get_median_side([self.Length, self.Height, self.Width])
        self.LengthGirth = get_length_girth_number([self.Length, self.Width])
        self.Timestamp = datetime.datetime.utcnow()

    def get_weight_estimate(self):  # , length, height, pages, binding):

        reamSize = 2000.0  # paper ream size
        paperSquareIn = 93.5  # square inches in a 8.5x11 paper
        paperWeight = 10.0  # paper grade
        ozInLb = 16.0  # ounces in pound

        paperReamWeightlbs = paperWeight  # 60lbs per ream estimate
        paperReamWeightOz = paperReamWeightlbs * ozInLb  # convert paper lbs to paper ozs
        perPaperOz = paperReamWeightOz / reamSize  # convert ream to per paper weight
        perSquareInOz = perPaperOz / paperSquareIn  # convert per paper oz to per paper square in oz

        bookSquareIn = self.Length * self.Height  # get the square inches of the book
        perPageOz = perSquareInOz * bookSquareIn  # multiply square inches of book by per square inch weight
        bookPaperWeight = perPageOz * self.Pages  # multiply page count by per page oz estimate
        hardCoverAdjustment = 1.5
        softCoverAdjustment = 0

        if self.BookBinding == 'Hardcover':
            return round(bookPaperWeight + hardCoverAdjustment, 4)
        else:
            return round(bookPaperWeight + softCoverAdjustment, 4)

    def get_size_estimate(self):

        if self.LongestSide < 15.0 and self.MedianSide < 12.0 and self.ShortestSide < 0.75 and self.ShippedWeightOz < 12.0:
            return 'Small standard-size'
        elif self.LongestSide < 18.0 and self.MedianSide < 14.0 and self.ShortestSide < 8.0 and self.ShippedWeightLbs < 20.0:
            return 'Large standard-size'
        elif self.LongestSide < 60.0 and self.MedianSide < 30.0 and self.LengthGirth < 130.0 and self.ShippedWeightLbs < 70.0:
            return 'Small oversize'
        elif self.LongestSide < 108.0 and self.LengthGirth < 130.0 and self.ShippedWeightLbs < 150.0:
            return 'Medium oversize'
        elif self.LongestSide < 108.0 and self.LengthGirth < 165.0 and self.ShippedWeightLbs < 150.0:
            return 'Large oversize'
        else:
            return 'Special oversize'

    def get_fufillment_fee_estimate(self):

        WeightLbs = self.ShippedWeightLbs
        month = self.Timestamp.month
        sizeEstimate = self.get_size_estimate()

        if 1 <= month < 10:
            if sizeEstimate == 'Small standard-size':
                return 2.41
            elif sizeEstimate == 'Large standard-size':
                if WeightLbs <= 1.0:
                    return 2.99
                elif 1 < WeightLbs <= 2.0:
                    return 4.18
                else:
                    return 4.18 + 0.39 * math.ceil(WeightLbs - 2.0)
        elif 10 <= month < 13:
            if sizeEstimate == 'Small standard-size':
                return 2.39
            elif sizeEstimate == 'Large standard-size':
                if WeightLbs <= 1.0:
                    return 2.88
                elif 1 < WeightLbs <= 2.0:
                    return 3.96
                else:
                    return 3.96 + 0.35 * math.ceil(WeightLbs - 2.0)
        else:
            return 10.0


    def get_storage_fee_estimate(self):

        month = self.Timestamp.month
        length = self.Length
        width = self.Width
        height = self.Height
        cubicIn = length * width * height
        cubicFt = cubicIn / 1728 #  number of cubic inches

        if 1 <= month < 10:
            return round(0.64 * cubicFt, 4)
        elif 10 < month <= 12:
            return round(2.35 * cubicFt, 4)
        else:
            return 10.0


    def get_total_fee_estimate(self):

        fufillmentFee = self.get_fufillment_fee_estimate()
        storageFee = self.get_storage_fee_estimate()

        return fufillmentFee + storageFee


book = bookers('9781524797027')

print('Longest side: ' + str(book.LongestSide))
print('Shortest side: ' + str(book.ShortestSide))
print('Median side: ' + str(book.MedianSide))
print('LengthGirth side: ' + str(book.LengthGirth))
print('Pages: ' + str(book.Pages))
print('Size estimate: ' + book.get_size_estimate())
print('Weight estimate: ' + str(book.get_weight_estimate()))
print('Shipped weight: ' + str(book.ShippedWeightOz))
print('Fufillment fee: ' + str(book.get_fufillment_fee_estimate()))
print('Storage fee: ' + str(book.get_storage_fee_estimate()))
print('Total fee: ' + str(book.get_total_fee_estimate()))

orders_api = mws.Orders(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
products_api = mws.Products(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
feeds_api = mws.Feeds(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
inventory_api = mws.Inventory(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
error_api = mws.MWSError()
recs_api = mws.Recommendations(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
reports_api = mws.Reports(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
sellers_api = mws.Sellers(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')

# root = ET.fromstring(products_api.get_matching_product(marketplaceid='ATVPDKIKX0DER',asins=[book.ASIN]).response.text)
# tree = ET.ElementTree(root)
# tree.write('deargirl.xml')

# '0134475585'
# '9780134475585'
# '9781101873724'
# '9781250158062'
# '1250158060'
# '9780062422507' dear girl
#  '9781250169730' Oliver loving
#  '9781524797027' need to know

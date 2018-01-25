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
products_api = mws.Products(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')


class MwsCall:
    def get_xml_response(self):
        test_call = products_api.get_competitive_pricing_for_asin(asins='1250158060', marketplaceid='ATVPDKIKX0DER')
        return test_call.original


class AmazonCall:

    def get_XML_response(isbn, group):
        try:
            return amazon.ItemLookup(ItemId=isbn,
                                     SearchIndex='Books',
                                     IdType='ISBN',
                                     ResponseGroup=group)
        except Exception as e:
            return ''

    def get_asin_XML_response(asin, group):
        try:
            return amazon.ItemLookup(ItemId=asin,
                                     SearchIndex='Books',
                                     IdType='ASIN',
                                     ResponseGroup=group)
        except Exception as e:
            return ''

    def create_root(xml):
        try:
            return ET.fromstring(xml)
        except Exception as e:
            return ''

    def get_total_new_offers(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalNew', namespaces=namespace)[0].text
        except Exception as e:
            return 999.0

    def get_total_used_offers(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:TotalUsed', namespaces=namespace)[0].text
        except Exception as e:
            return 999.0

    def get_lowest_new_price(root, namespace):
        try:
            return \
            float(root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestNewPrice/ns0:Amount', namespaces=namespace)[
                0].text / 100.0)
        except Exception as e:
            return .99

    def get_lowest_used_price(root, namespace):
        try:
            return \
            root.findall('ns0:Items/ns0:Item/ns0:OfferSummary/ns0:LowestUsedPrice/ns0:Amount', namespaces=namespace)[
                0].text / 100.0
        except Exception as e:
            return .99

    def get_buy_box_merchant(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:Merchant/ns0:Name', namespaces=namespace)[
                0].text
        except Exception as e:
            return ''

    def get_new_buy_box_price(root, namespace):
        try:
            if root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferAttributes/ns0:Condition', namespaces=namespace)[0].text == 'New':
                return float(root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferListing/ns0:Price/ns0:Amount', namespaces=namespace)[0].text) / 100.0
            elif root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferAttributes/ns0:Condition', namespaces=namespace)[1].text == 'New':
                return float(root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferListing/ns0:Price/ns0:Amount', namespaces=namespace)[1].text) / 100.0
            if root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferAttributes/ns0:Condition', namespaces=namespace)[2].text == 'New':
                return float(root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferListing/ns0:Price/ns0:Amount', namespaces=namespace)[2].text) / 100.0
            else:
                return 0
        except Exception as e:
            return 0

    def get_used_buy_box_price(root, namespace):
        try:
            if root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferAttributes/ns0:Condition', namespaces=namespace)[0].text == 'Used':
                return float(root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferListing/ns0:Price/ns0:Amount', namespaces=namespace)[0].text) / 100.0
            elif root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferAttributes/ns0:Condition', namespaces=namespace)[1].text == 'Used':
                return float(root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferListing/ns0:Price/ns0:Amount', namespaces=namespace)[1].text) / 100.0
            if root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferAttributes/ns0:Condition', namespaces=namespace)[2].text == 'Used':
                return float(root.findall('ns0:Items/ns0:Item/ns0:Offers/ns0:Offer/ns0:OfferListing/ns0:Price/ns0:Amount', namespaces=namespace)[2].text) / 100.0
            else:
                return 0
        except Exception as e:
            return 0

    def get_asin(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:ASIN', namespaces=namespace)[0].text
        except Exception as e:
            return ''

    def get_sales_rank(root, namespace):
        try:
            return int(root.findall('ns0:Items/ns0:Item/ns0:SalesRank', namespaces=namespace)[0].text)
        except Exception as e:
            return 0

    def get_author(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Author', namespaces=namespace)[0].text
        except Exception as e:
            return ''

    def get_book_binding(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Binding', namespaces=namespace)[0].text
        except Exception as e:
            return ''

    def get_publisher(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Publisher', namespaces=namespace)[0].text
        except Exception as e:
            return ''

    def get_pages(root, namespace):
        try:
            return float(
                root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:NumberOfPages', namespaces=namespace)[0].text)
        except Exception as e:
            return 0

    def get_publication_date(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:PublicationDate', namespaces=namespace)[
                0].text
        except Exception as e:
            return ''

    def get_list_price(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ListPrice/ns0:Amount', namespaces=namespace)[
                0].text
        except Exception as e:
            return 0

    def get_weight(root, namespace):
        try:
            return \
                root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Weight',
                             namespaces=namespace)[
                    0].text / 100.0
        except Exception as e:
            100.0

    def get_height(root, namespace):
        try:
            return int(
                root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Height',
                             namespaces=namespace)[
                    0].text) / 100.0
        except Exception as e:
            return 0

    def get_length(root, namespace):
        try:
            return int(
                root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Length',
                             namespaces=namespace)[
                    0].text) / 100.0
        except Exception as e:
            return 0

    def get_width(root, namespace):
        try:
            return int(
                root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:ItemDimensions/ns0:Width',
                             namespaces=namespace)[
                    0].text) / 100.0
        except Exception as e:
            return 0

    def get_title(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:Title', namespaces=namespace)[0].text
        except Exception as e:
            return ''

    def get_amazon_trade_value(root, namespace):
        try:
            return \
            root.findall('ns0:Items/ns0:Item/ns0:ItemAttributes/ns0:TradeInValue/ns0:Amount', namespaces=namespace)[
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
            return ''

    def get_small_image_height(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:Height', namespaces=namespace)[0].text
        except Exception as e:
            return 0

    def get_small_image_width(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:SmallImage/ns0:Width', namespaces=namespace)[0].text
        except Exception as e:
            return 0

    def get_medium_image_url(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:URL', namespaces=namespace)[0].text
        except Exception as e:
            return ''

    def get_medium_image_height(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:Height', namespaces=namespace)[0].text
        except Exception as e:
            return 0

    def get_medium_image_width(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:MediumImage/ns0:Width', namespaces=namespace)[0].text
        except Exception as e:
            return 0

    def get_large_image_url(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:URL', namespaces=namespace)[0].text
        except Exception as e:
            return ''

    def get_large_image_height(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:Height', namespaces=namespace)[0].text
        except Exception as e:
            return 0

    def get_large_image_width(root, namespace):
        try:
            return root.findall('ns0:Items/ns0:Item/ns0:LargeImage/ns0:Width', namespaces=namespace)[0].text
        except Exception as e:
            return 0

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
            return 0.0


class Item(object):
    def __init__(self, isbn):
        self.Isbn = isbn
        self.NameSpace = {'ns0': 'http://webservices.amazon.com/AWSECommerceService/2013-08-01'}
        self.OfferXMLResponse = AmazonCall.get_XML_response(isbn=self.Isbn, group='OfferFull')
        self.OfferRoot = AmazonCall.create_root(xml=self.OfferXMLResponse)
        self.RankXMLResponse = AmazonCall.get_XML_response(isbn=self.Isbn, group='SalesRank')
        self.RankRoot = AmazonCall.create_root(xml=self.RankXMLResponse)
        self.ItemXMLResponse = AmazonCall.get_XML_response(isbn=self.Isbn, group='ItemAttributes')
        self.ItemRoot = AmazonCall.create_root(xml=self.ItemXMLResponse)
        self.ImageXMLResponse = AmazonCall.get_XML_response(isbn=self.Isbn, group='Images')
        self.ImageRoot = AmazonCall.create_root(xml=self.ImageXMLResponse)

        self.TotalNewOffers = AmazonCall.get_total_new_offers(root=self.OfferRoot, namespace=self.NameSpace)
        self.TotalUsedOffers = AmazonCall.get_total_used_offers(root=self.OfferRoot, namespace=self.NameSpace)
        self.LowestNewPrice = AmazonCall.get_lowest_new_price(root=self.OfferRoot, namespace=self.NameSpace)
        self.LowestUsedPrice = AmazonCall.get_lowest_used_price(root=self.OfferRoot, namespace=self.NameSpace)
        self.BuyBoxMerchant = AmazonCall.get_buy_box_merchant(root=self.OfferRoot, namespace=self.NameSpace)
        self.ASIN = AmazonCall.get_asin(root=self.RankRoot, namespace=self.NameSpace)
        self.SalesRank = AmazonCall.get_sales_rank(root=self.RankRoot, namespace=self.NameSpace)
        self.Author = AmazonCall.get_author(root=self.ItemRoot, namespace=self.NameSpace)
        self.BookBinding = AmazonCall.get_book_binding(root=self.ItemRoot, namespace=self.NameSpace)
        self.Publisher = AmazonCall.get_publisher(root=self.ItemRoot, namespace=self.NameSpace)
        self.Pages = AmazonCall.get_pages(root=self.ItemRoot, namespace=self.NameSpace)
        self.PublicationDate = AmazonCall.get_publication_date(root=self.ItemRoot, namespace=self.NameSpace)
        self.ListPrice = AmazonCall.get_list_price(root=self.ItemRoot, namespace=self.NameSpace)
        self.Weight = AmazonCall.get_weight(root=self.ItemRoot, namespace=self.NameSpace)
        self.Height = AmazonCall.get_height(root=self.ItemRoot, namespace=self.NameSpace)
        self.Length = AmazonCall.get_length(root=self.ItemRoot, namespace=self.NameSpace)
        self.Width = AmazonCall.get_width(root=self.ItemRoot, namespace=self.NameSpace)
        self.Title = AmazonCall.get_title(root=self.ItemRoot, namespace=self.NameSpace)
        self.ShippedWeightLbs = AmazonCall.get_shipped_weight(root=self.ItemRoot, namespace=self.NameSpace)
        self.ShippedWeightOz = AmazonCall.get_shipped_weight(root=self.ItemRoot, namespace=self.NameSpace) * 16.0
        self.TradeInStatus = AmazonCall.get_amazon_trade_status(root=self.ItemRoot, namespace=self.NameSpace)
        self.TradeInValue = AmazonCall.get_amazon_trade_value(root=self.ItemRoot, namespace=self.NameSpace)
        self.SmallImageUrl = AmazonCall.get_small_image_url(root=self.ImageRoot, namespace=self.NameSpace)
        self.SmallImageHeight = AmazonCall.get_small_image_height(root=self.ImageRoot, namespace=self.NameSpace)
        self.SmallImageWidth = AmazonCall.get_small_image_width(root=self.ImageRoot, namespace=self.NameSpace)
        self.MediumImageUrl = AmazonCall.get_medium_image_url(root=self.ImageRoot, namespace=self.NameSpace)
        self.MediumImageHeight = AmazonCall.get_medium_image_height(root=self.ImageRoot, namespace=self.NameSpace)
        self.MediumImageWidth = AmazonCall.get_medium_image_width(root=self.ImageRoot, namespace=self.NameSpace)
        self.LargeImageUrl = AmazonCall.get_large_image_url(root=self.ImageRoot, namespace=self.NameSpace)
        self.LargeImageHeight = AmazonCall.get_large_image_height(root=self.ImageRoot, namespace=self.NameSpace)
        self.LargeImageWidth = AmazonCall.get_large_image_width(root=self.ImageRoot, namespace=self.NameSpace)
        self.LongestSide = AmazonCall.get_longest_side([self.Length, self.Height, self.Width])
        self.ShortestSide = AmazonCall.get_shortest_side([self.Length, self.Height, self.Width])
        self.MedianSide = AmazonCall.get_median_side([self.Length, self.Height, self.Width])
        self.LengthGirth = AmazonCall.get_length_girth_number([self.Length, self.Width])
        self.AsinSearchXMLResponse = AmazonCall.get_asin_XML_response(asin=self.ASIN, group='OfferFull')
        self.AsinOfferRoot = AmazonCall.create_root(xml=self.AsinSearchXMLResponse)
        self.NewBuyBoxPrice = AmazonCall.get_new_buy_box_price(root=self.AsinOfferRoot, namespace=self.NameSpace)
        self.UsedBuyBoxPrice = AmazonCall.get_used_buy_box_price(root=self.AsinOfferRoot, namespace=self.NameSpace)
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

    def get_fulfillment_fee_estimate(self):

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
        cubicFt = cubicIn / 1728  # number of cubic inches

        if 1 <= month < 10:
            return round(0.64 * cubicFt, 4)
        elif 10 < month <= 12:
            return round(2.35 * cubicFt, 4)
        else:
            return 10.0

    def get_total_fee_estimate(self):

        fufillmentFee = self.get_fulfillment_fee_estimate()
        storageFee = self.get_storage_fee_estimate()

        return fufillmentFee + storageFee

#
# orders_api = mws.Orders(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
# feeds_api = mws.Feeds(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
# inventory_api = mws.Inventory(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
# error_api = mws.MWSError()
# recs_api = mws.Recommendations(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
# reports_api = mws.Reports(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')
# sellers_api = mws.Sellers(access_key=MWSAccessKey, secret_key=MWSSecretKey, account_id=MWSAccountID, region='US')

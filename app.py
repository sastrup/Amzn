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

response = amazon.ItemLookup(ItemId='9781101873724',
                             IdType='ISBN',
                             SearchIndex='Books',
                             ResponseGroup='Offers')

ns = {'def': '{http://webservices.amazon.com/AWSECommerceService/2013-08-01}'}

root = ET.fromstring(response)

print(root.findall('.//def:OperationRequest', namespaces=ns))


# for child in root:
#     for i in child:
#         if i.tag != '{http://webservices.amazon.com/AWSECommerceService/2013-08-01}Request':
#             pass
#         else:
#             for RequestItem in i:
#                 print(RequestItem.tag)
#
#



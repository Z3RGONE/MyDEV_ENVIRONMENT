from http.client import HTTPResponse
from io import BytesIO
import os
import pandas as pd
import re


def getResponseParts(fulltpath):
    file = open (fulltpath, "r")
    lines = file.read() #.replace('\n',';')
    file.close()

    pattern = re.compile("(--ejjeeffe\d\s[a-zA-Z]+[-][a-zA-Z]+[:]\s[a-zA-Z/]+\n[a-zA-Z-:]+\s\d+\n[a-zA-Z-:]+\s[a-zA-Z]+\n)|(--ejjeeffe\d--\n)")
    matches = re.split(pattern, lines)

    response = []
    for match in matches:
        if match is not None:
            if "ejjeeffe" not in match and len(match)>2 :
                if match.startswith("""{"d":{""",1,6):
                    os.linesep + match
                    response.append(os.linesep + match)
                else:
                    response.append(match)
                # check = True
                # print("Match:  {}, {}".format(check, match ))   
            # else:
            #     check = False 
            #     print("Match:  {}, {}".format(check, match ))   
    
        
    return response

def main2():
    df = pd.read_csv(os.path.join("C:\TEMP", "22110199_Response_20221171325.json"), sep="--ejjeeffe1", header=None)
    print(df)


def getDetailsFromPart(http_response_str):
    # http_response_str = """HTTP/1.1 201 Created
    # Content-Type: application/json
    # Content-Length: 1498
    # location: https://my353666.sapbydesign.com/sap/byd/odata/cust/v1/workbench/ShippingProviderTransportOrderItemRootCollection('FA163EB4F3841EED97D2EAF125D9302E')      
    # dataserviceversion: 2.0
    # cache-control: no-cache, no-store

    # {"d":{"results":{"__metadata":{"uri":"https://my353666.sapbydesign.com/sap/byd/odata/cust/v1/workbench/ShippingProviderTransportOrderItemRootCollection('FA163EB4F3841EED97D2EAF125D9302E')","type":"cust.ShippingProviderTransportOrderItemRoot"},"ObjectID":"FA163EB4F3841EED97D2EAF125D9302E","ID":"724253","EasyMailOrderNumber":"22110199","DeliveryDate":"\/Date(1667520000000)\/","DeliveryPartnerInternalID":"6300014434","CustomerInternalID":"6300014290","Currency":"EUR","CurrencyText":"Euro","CompanyID":"1000000000","Quantity":"30.00000000000000","QuantityUnitCode":"EA","QuantityUnitCodeText":"Each","UnloadingPoint":"","PickUpDate":"\/Date(1667433600000)\/","LoadingPoint":"","ProductInternalID":"10074","LastChangeDateTime":"\/Date(1667823962922)\/","Weight":"0.36500000000000","WeightUnitCode":"KGM","WeightUnitCodeText":"Kilogram","CreationDateTime":"\/Date(1667823962922)\/","ExternalUUID":"4907765E-5B2B-45ED-A1FA-0C294C993F30","DeliveryPartnerWeight":"0.36500000000000","DeliveryPartnerWeightUnitCode":"KGM","DeliveryPartnerWeightUnitCodeText":"Kilogram","DeliveryPartnerProductInternalID":"10074","DeliveryPartnerQuantity":"30.00000000000000","DeliveryPartnerQuantityUnitCode":"EA","DeliveryPartnerQuantityUnitCodeText":"Each","Object":"704417","Version":"14570","CostCentreID":"1106040004","PurchaseOrderProcessingStatusCode":"1","PurchaseOrderProcessingStatusCodeText":"Open","SalesOrderProcessingStatusCode":"1","SalesOrderProcessingStatusCodeText":"Open","MassUpdateIndicator":false}}}
    # """

    resultSet = None

    http_response_bytes = http_response_str.encode()

    class FakeSocket():
        def __init__(self, response_bytes):
            self._file = BytesIO(response_bytes)
        def makefile(self, *args, **kwargs):
            return self._file

    
    try:
        source = FakeSocket(http_response_bytes)
        response = HTTPResponse(source)
        response.begin()
        
        resultSet = {
            "status": response.status,
            "single header": response.getheader('Content-Type'),
            "content":response.read(len(http_response_str))
        }
    except Exception as error:
        print("An error occured" + str(error))

    return resultSet
    # print( "status:", response.status)
    # status: 200
    # print( "single header:", response.getheader('Content-Type'))
    # single header: text/xml; charset="utf-8"
    # print( "content:", response.read(len(http_response_str)))
    # content: b'teststring'
    # print( "date:", response.getheader('Date'))


def main():    
    parts = getResponseParts(os.path.join("C:\TEMP", "22110199_Response_20221171325.json"))
    for p in parts:
            # print(p)
            tmp = getDetailsFromPart(p)
            print(tmp)

if __name__ == "__main__":
    main()

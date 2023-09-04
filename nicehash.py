import urllib.parse
import urllib.request
import json

class NiceHashAPI:
    def __init__(self):
        self.apiUrl = 'https://api-test.nicehash.com'
        
    
    
    def query(self, route):
        req = urllib.request.Request(self.apiUrl+route)
        try:
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
                return the_page
        except EnvironmentError:
            return 500

    def queryWithData(self, route, json):
        data = urllib.parse.urlencode(json)
        data = data.encode('ascii') # data should be bytes
        url = self.apiUrl+route
        req = urllib.request.Request(url, data)
        try:
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
                return the_page
        except EnvironmentError:
            return 500

    def getAlgos(self):
        return self.query("/main/api/v2/mining/algorithms")

    def getOptimalPrice(self, market, algo):
        json = {
            "market":market,
            "algorithm":algo
        }
        return self.query("/main/api/v2/hashpower/order/price"+urllib.parse.urlencode(json))

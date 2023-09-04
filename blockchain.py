# Blockchain.com API for BTC data

import urllib.parse
import urllib.request
import time
import json

DEBUG_MODE = True

class BlockchainQueryAPI:
    def __init__(self):
        self.apiUrl = 'https://blockchain.info/q'
        self.lastQuery = time.time()-10
        self.blockHeight = -1
        self.avgBlockTimeSeconds = -1
        self.difficulty = -1
        self.blockReward = -1
        self.globalHashRate = -1
        
    
    #Docs require rate limiting to 10s or more between calls to API
    def ratelimit(self):
        delta = time.time() - self.lastQuery
        if(delta < 10):
            print(f'Too fast, need to wait {10-delta} seconds')
            time.sleep(10-delta)
        else:
            print(f'{delta}s since last query, proceed.')
        return

    def query(self, route):
        self.ratelimit()
        queryTime = time.time()
        req = urllib.request.Request(self.apiUrl+route)
        self.lastQuery = queryTime
        try:
            with urllib.request.urlopen(req) as response:
                the_page = response.read()
                if DEBUG_MODE:
                    print(f'{route}: {the_page.decode()}')
                return the_page
        except EnvironmentError:
            return 500

    def queryWithData(self, route, json):
        self.ratelimit
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



    def updateBlockHeight(self):
        self.blockHeight = int(self.query(f'/getblockcount'))
        return self.blockHeight

    def updateAvgBlockTime(self):
        self.avgBlockTimeSeconds = float(self.query(f'/interval'))

    def updateDifficulty(self):
        #Needs to be decoded to string, then multiply E notation
        response = self.query(f'/getdifficulty').decode()
        diff = response.split('E')
        num = float(diff[0])
        pow = int(diff[1])
        self.difficulty = num * 10**pow
        return self.difficulty
    
    def updateBlockReward(self):
        self.blockReward = float(self.query(f'/bcperblock'))
        return self.blockReward

    def updateAll(self):
        lastBlockHeight = self.blockHeight
        if self.updateBlockHeight() > lastBlockHeight:
            self.updateAvgBlockTime()
            self.updateDifficulty()
            self.updateBlockReward()
        

    def calculate24hMiningReward(self, hashRateTH):
        self.updateAll()
        blocks24h = (24 * 60 * 60) / self.avgBlockTimeSeconds
        self.globalHashRate = ( (blocks24h / 144) * self.difficulty * (2**32) ) / 600
        dailyReward = self.blockReward * 144
        hashRatePercent = hashRateTH * 10**12 / self.globalHashRate
        return dailyReward * hashRatePercent


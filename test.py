from nicehash import NiceHashAPI
from blockchain import BlockchainQueryAPI
import time
nh=NiceHashAPI()
btc = BlockchainQueryAPI()
#print(nh.getAlgos())
print(f'Mining reward for 140TH/s is {btc.calculate24hMiningReward(140)} BTC')

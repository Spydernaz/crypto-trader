import requests, os, time
import buildData as bd

slow_mode=True
dayDelta = 0
endtime = 1633289146 - (86400*dayDelta)
starttime = endtime - (86400*(dayDelta+1)) # 1 day

# Have 0 day delta
coinlist = {"btc":"bitcoin","eth":"ethereum","dot":"polkadot","ont":"ontology"}
# Remove Ontology as I already have this data for this run
# coinlist = {"btc":"bitcoin","eth":"ethereum","dot":"polkadot"}
coinlist = {"poly":"polymath-network","eos":"eos","hnt":"helium","omg":"omg","xtz":"tezos","sol":"solana","qnt":"quant"}


first = true # testing if it is the first key, therefore dont wait the ten minutes
# coindata = bd.coindata
print(f"Current coins = {bd.coindata.keys()}")
for coincode,coinname in coinlist.items():
    if coincode not in bd.coindata.keys():
        bd.coindata[coincode] = []
    if slow_mode and not first:
        first = False
        time.sleep(600)
    url = f"https://api.coincap.io/v2/candles?exchange=binance&interval=m1&baseId={coinname}&quoteId=tether&start={str(starttime)}000&end={str(endtime)}000"
    response = requests.request("GET", url, headers=headers, data=payload)
    try: 
        bd.coindata[coincode].extend(response.json()["data"])
    except:
        print(response.text)



file = open("./buildData.py", "w")
file.write(f"coindata={str(bd.coindata)}")
file.close()

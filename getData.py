import requests, os, time

slow_mode=True

coin="ontology"
coinlist = {"btc":"bitcoin","eth":"ethereum","dot":"polkadot","ont":"ontology"}

# headers={'Authorization': f'Bearer {coincap_api_key}'}
coincap_api_key=os.environ.get("coincap_api_key")

url = f"api.coincap.io/v2/assets/{coin}/history?interval=d1"
url = f"api.coincap.io/v2/candles?exchange=binance&interval=m1&baseId={coin}&quoteId=tether&start=1617033600000&end=1633190400000"
# url = f"api.coincap.io/v2/candles?exchange=binance&interval=h8&baseId={coin}&quoteId=tether"

payload = {}
headers={'Authorization': f'Bearer {coincap_api_key}'}

coindata = {}
for coincode,coinname in coinlist.items():
    if slow_mode:
        time.sleep(300)
    url = f"https://api.coincap.io/v2/candles?exchange=binance&interval=h8&baseId={coinname}&quoteId=tether&start=1617033600000&end=1633190400000"
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        coindata[coincode] = response.json()["data"]
    except:
        print(response.text)
    


file = open("./cryptodata.py", "w")
file.write(f"coindata={str(coindata)}")
file.close()

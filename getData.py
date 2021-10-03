import requests, os


coin="ontology"
coinlist = {"btc":"bitcoin","eth":"ethereum","dot":"polkadot","ont":"ontology"}

# headers={'Authorization': f'Bearer {coincap_api_key}'}
coincap_api_key=os.environ.get("coincap_api_key")

url = f"api.coincap.io/v2/assets/{coin}/history?interval=d1"
url = f"api.coincap.io/v2/candles?exchange=binance&interval=h8&baseId={coin}&quoteId=tether&start=1617033600000&end=1633190400000"
# url = f"api.coincap.io/v2/candles?exchange=binance&interval=h8&baseId={coin}&quoteId=tether"

payload = {}
headers={'Authorization': f'Bearer {coincap_api_key}'}

coindata = {}
for coincode,coinname in coinlist.items():
    url = f"https://api.coincap.io/v2/candles?exchange=binance&interval=h8&baseId={coinname}&quoteId=tether&start=1617033600000&end=1633190400000"
    response = requests.request("GET", url, headers=headers, data=payload)
    coindata[coincode] = response.json()["data"]
    


file = open("./cryptodata.py", "w")
file.write(f"coindata={str(coindata)}")
file.close()

import requests, os, time
import buildData as bd

slow_mode=True

coinlist = {"btc":"bitcoin","eth":"ethereum","dot":"polkadot","ont":"ontology"}

coincap_api_key=os.environ.get("coincap_api_key")
coincap_api_key="c154b809-698a-4c3e-a72b-62cce835821f"

payload = {}
headers={'Authorization': f'Bearer {coincap_api_key}'}

coindata = {}
for coincode,coinname in coinlist.items():
    if slow_mode:
        time.sleep(300)
    url = f"https://api.coincap.io/v2/candles?exchange=binance&interval=h1&baseId={coinname}&quoteId=tether&start=1617033600000&end=1633190400000"
    response = requests.request("GET", url, headers=headers, data=payload)
    try: 
        coindata[coincode] = response.json()["data"]
    except:
        print(response.text)



file = open("./cryptodata.py", "w")
file.write(f"coindata={str(coindata)}")
file.close()

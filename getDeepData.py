import requests, os, time
import deeperData as bd

slow_mode=True
first = True # testing if it is the first key, therefore dont wait the ten minutes

# coincap_api_key=os.environ.get("coincap_api_key")
coincap_api_key="c154b809-698a-4c3e-a72b-62cce835821f"
payload = {}
headers={'Authorization': f'Bearer {coincap_api_key}'}

for i in range(14):
    endtime = 1633289146 - (86400*i) # (i) days from Monday, October 4
    starttime = endtime - (86400) # 1 day time difference

    # Have 0 day delta
    coinlist = {"btc":"bitcoin","eth":"ethereum","dot":"polkadot","ont":"ontology","poly":"polymath-network","eos":"eos","hnt":"helium","omg":"omg","xtz":"tezos","sol":"solana","qnt":"quant"}

    print(f"Current coins = {bd.coindata.keys()}")

    for coincode,coinname in coinlist.items():
        print(f"Currently working on {coinname}")
        if coincode not in bd.coindata.keys():
            bd.coindata[coincode] = []
        # if slow_mode and not first:
        #     time.sleep(600)
        url = f"https://api.coincap.io/v2/candles?exchange=binance&interval=m1&baseId={coinname}&quoteId=tether&start={str(starttime)}000&end={str(endtime)}000"
        temp_code = -200
        while temp_code != 200:
            response = requests.request("GET", url, headers=headers, data=payload)
            temp_code = response.status_code
            print(f"\tStatus Code: {response.status_code}")
            if response.status_code == 200:
                print(f"\tPayload Length: {len(response.json()['data'])}")
                bd.coindata[coincode].extend(response.json()["data"])
            else:
                print(response.text)
                time.sleep(60)
        first = False
    file = open("./deeperData.py", "w")
    file.write(f"coindata={str(bd.coindata)}")
    file.close()
    time.sleep(120)



file = open("./deeperData.py", "w")
file.write(f"coindata={str(bd.coindata)}")
file.close()

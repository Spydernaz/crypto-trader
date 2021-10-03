import staticdata_ohlcvp as sd


file = open("./cryptodata", "w")
file.write(f"coins={str(sd.coins)}")
file.close()
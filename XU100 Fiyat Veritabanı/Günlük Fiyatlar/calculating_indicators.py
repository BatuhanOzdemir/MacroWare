import pymongo


xu100_stocks =['AEFES',  'AGHOL',  'AGROT', 'AKBNK', 'AKFGY', 'AKFYE',
  'AKSA',   'AKSEN',  'ALARK', 'ALFAS', 'ARCLK', 'ARDYZ',
  'ASELS',  'ASTOR',  'BERA',  'BFREN', 'BIMAS', 'BINHO',
  'BRSAN',  'BRYAT',  'BTCIM', 'CANTE', 'CCOLA', 'CIMSA',
  'CWENE',  'DOAS',   'DOHOL', 'ECILC', 'ECZYT', 'EGEEN',
  'EKGYO',  'ENERYA', 'ENJSA', 'ENKAI', 'EREGL', 'EUPWR',
  'EURPEN', 'FROTO',  'GARAN', 'GESAN', 'GOLTS', 'GUBRF',
  'HALKB',  'HEKTS',  'ISCTR', 'ISGYO', 'ISMEN', 'IZENR',
  'KAYSE',  'KCAER',  'KCHOL', 'KLSER', 'KONTR', 'KONYA',
  'KOZAA',  'KOZAL',  'KRDMD', 'KTLEV', 'LMKDC', 'MAVI',
  'MGROS',  'MIATK',  'OBAMS', 'ODAS',  'OTKAR', 'OYAKC',
  'PEKGY',  'PETKM',  'PGSUS', 'QUAGR', 'REEDR', 'SAHOL',
  'SASA',   'SDTTR',  'SISE',  'SKBNK', 'SMRTG', 'SOKM',
  'TABGD',  'TAVHL',  'TCELL', 'THYAO', 'TKFEN', 'TKNSA',
  'TMSN',   'TOASO',  'TSKB',  'TTKOM', 'TTRAK', 'TUKAS',
  'TUPRS',  'TURSG',  'ULKER', 'VAKBN', 'VESBE', 'VESTL',
  'YEOTK',  'YKBNK',  'YYGLD', 'ZOREN']

def read():
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["Bist_Price_Data"]
	collection = db["xu100_Daily_Prices"]
	x = collection.find({"Kapanış":1},{"Ağırlıklı_Ortalama":1})
	for price in x:
		pass

def ema(price):#exponential moving average


import pandas as pd
import os
import pymongo



def write_stocks():
	#Establishing connection with Mongodb
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["Bist_Price_Data"]
	collection = db["xu100_Daily_Prices"]

	#Reading the excel files
	path_to_files ="C:\\Users\\batuh\\Desktop\\Bist Veritabanı\\MacroWare\\XU100 Fiyat Veritabanı\\XU100 Fiyat Verileri\\Günlük Yeni"
	os.chdir(path_to_files)
	for name in os.listdir(path_to_files):
		pd.options.display.float_format = '{:.0f}'.format
		df = pd.read_excel(name)
		for index,row in df.iterrows():
			dict_to_insert = {"Hisse_Kodu":name.strip(".xlsx"),"Tarih":row["Tarih"],
			                  "Açılış":row["Açılış"],"Yüksek":row["Yüksek"],"Düşük":row["Düşük"],
			                  "Kapanış":row["Kapanış"],"Ağırlıklı Ortalama":row["Ağırlıklı Ortalama"],
			                  "Miktar":row["Miktar"],"Hacim":row["Hacim"]}
			x = collection.insert_one(dict_to_insert)
			print(x)


def write_indicies():
	#Endeksler
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	db = client["Bist_Price_Data"]
	collection = db["Bist_Indicies"]

	path_to_files ="C:\\Users\\batuh\\Desktop\\Bist Veritabanı\\MacroWare\\XU100 Fiyat Veritabanı\\XU100 Fiyat Verileri\\Endeksler"
	os.chdir(path_to_files)
	for name in os.listdir(path_to_files):
		pd.options.display.float_format = '{:.0f}'.format
		df = pd.read_excel(name)
		for index,row in df.iterrows():
			dict_to_insert = {"Endeks":name.strip(".xlsx"),"Tarih":row["Tarih"],
			                  "Açılış":row["Açılış"],"Yüksek":row["Yüksek"],"Düşük":row["Düşük"],
			                  "Kapanış":row["Kapanış"],"Ağırlıklı Ortalama":row["Ağırlıklı Ortalama"],
			                  "Miktar":row["Miktar"],"Hacim":row["Hacim"]}
			x = collection.insert_one(dict_to_insert)
			print(x)

if __name__ == "__main__":
	write_stocks()
	write_indicies()
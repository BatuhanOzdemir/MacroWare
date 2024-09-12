#Work in Progress!!
import time
from datetime import date
import pandas as pd
from evds import evdsAPI
import subprocess
from pathlib import Path
import datetime
import os
import tqdm
import pymongo



formula_explanation = {1:"Yüzde Değişimi",2:"Fark",3:"Yıllık Yüzde Değişim",4:"Yıllık Fark",5:"Bir önceki yılın sonuna göre yüzdelik değişim",6:"Bir önceki yılın sonuna göre fark",7:"Hareketli Ortalama",8:"Hareketli Toplam"}

def remove_illegal_characters(filename) -> str:
	illegal_characters = ["<", ">", ":", "/", "\\", "|", "?"]
	allowed_filename = "".join(ch for ch in filename if ch.isalnum())
	return allowed_filename
def read_data(filter) -> list:
	client = pymongo.MongoClient("mongodb://localhost:27017/")#Veritabanına bağlanıyoruz
	db = client["Macroeconomics"]
	collection = db["TCMB"]
	x = collection.find({filter},{"Veri":1})#Burdaki Collection SQL deki table ile aynı, yani table'dan "Veri" sütünunu alıyoruz
	df_list = []
	for json in x:#"Veri sütünundaki her Json için
		df = pd.read_json(path_or_buf=json["Veri"],orient="index",typ="frame")#Veritabanından okurken "Veri" sütünundaki veriler bit dict olarak geliyor bu dict iki key'e sahip "Id" Object Id ye karşılık geliyor "Veri" ise Json str oluyor
		df_list.append(df)
	return df_list


def write_to_db(evds) -> None:
	client = pymongo.MongoClient("mongodb://localhost:27017/")#mongodb ile bağlantı kuruyor
	db = client["Macroeconomics"]#çalışmak istediğin veritabanını seçiyorsun
	collection = db["TCMB"]#burdaki collection SQL deki Table ile aynı şey, yani Table seçiyoruz
	for category in evds.main_categories.iterrows():#Ana Kategorileri itere eden for döngüsü a.k.a main loop
		sub_category_codes = evds.get_sub_categories(category[1].array[0]).get("DATAGROUP_CODE")#Group Code ile itere edebiliyoruz
		sub_category_names = evds.get_sub_categories(category[1].array[0]).get("DATAGROUP_NAME")#Verittabanına anlamlı bir şekilde yazabilmek için alt kategorilerin kategorinin  adını alıyoruz
		for i, code in enumerate(sub_category_codes):#Alt Kategorileri itere ediyoruz
			for seri in evds.get_series(code).values:#Serileri itere ediyoruz
				seri_kodu = seri[0]
				seri_adı = seri[1]
				seri_baslangıc_tarihi = seri[2]
				Ana_kategori = category[1].array[1]#Veritabanına yazmak için Ana kategori ismini alıyoruz
				Alt_kategori = sub_category_names[i]#Aynı şekilde Alt Kategori isminide alıyoruz
				try:
					for j in range(1,9):#get_data() fonksiyonundaki formulas parametresine 1 den 8 e kadar tüm değerleri verip veritabanına kaydediyoruz
						seri_df = evds.get_data(series=[seri_kodu],startdate=seri_baslangıc_tarihi,enddate=datetime.date.today().strftime("%d-%m-%Y"),
						                          formulas=str(j))
						seri_json = seri_df.to_json(orient="index",index=True)
						dict_to_insert = {"Ana_Kategori":Ana_kategori,"Alt_Kategori":Alt_kategori,"Seri_Adı":seri[1],
						                  "Veri Formülü":formula_explanation[j],"Başlangıç Tarihi":seri_baslangıc_tarihi,"Bitiş Tarihi":datetime.date.today().strftime("%d-%m-%Y"),
						                  "Veri":seri_json}#burdaki veri türü formulas parametresine verdiğimiz değere göre değişiyor
						if collection.count_documents({"Ana_Kategori":Ana_kategori,"Alt_Kategori":Alt_kategori,"Seri_Adı":dict_to_insert["Seri_Adı"],"Veri Formülü":formula_explanation[j]},limit=2) <= 0:#entry daha önceden kayıtlımı diye bakıyoruz
							x = collection.insert_one(dict_to_insert)
						else:
							pass
						print(x)#Yazma işlemi başarıyla gerçekleştiyse konsola yazdırılıyor aksi halde hata veriyor
				except Exception as e:
					if str(e).__contains__("Read timed out."):
							time.sleep(10)
							seri_df = evds.get_data(series=[seri_kodu], startdate=seri_baslangıc_tarihi,
							                        enddate=datetime.date.today().strftime("%d-%m-%Y"),
							                        formulas=str(j))
							seri_json = seri_df.to_json(orient="index", index=True)
							dict_to_insert = {"Ana_Kategori": Ana_kategori, "Alt_Kategori": Alt_kategori,
							                  "Seri_Adı": seri[1],
							                  "Veri Formülü": formula_explanation[j],
							                  "Başlangıç Tarihi": seri_baslangıc_tarihi,
							                  "Bitiş Tarihi": datetime.date.today().strftime("%d-%m-%Y"),
							                  "Veri": seri_json}  # burdaki veri türü formulas parametresine verdiğimiz değere göre değişiyor
							if collection.count_documents(
									{"Ana_Kategori":Ana_kategori,"Alt_Kategori":Alt_kategori,"Seri_Adı":dict_to_insert["Seri_Adı"],"Veri Formülü":formula_explanation[j]},limit=2) <= 0:
								x = collection.insert_one(dict_to_insert)
							else:
								continue
							print(x)
							continue
					else:
						print(e)




def get_macro_info(evds,main_directory) -> None:

	print("\n\nProgress on the data collection\n")
	print("\nBeware the process is quite long!\n\n")
	print("\n")

	pbar_main = tqdm.tqdm(desc="Main Category",total=evds.main_categories.shape[0])#Progress bar
	for category in evds.main_categories.iterrows():#start to iterate every main category
		try:
			os.chdir(main_directory)#make the cwd main directory
			folder_main = Path(Path.cwd(),category[1].array[1])#get the main category name and create the folder for the main category
			if not os.path.exists(folder_main):
				os.mkdir(folder_main)#Ana kategori adı ile cwd de bir klasör oluşturuyor
			data_group_code = evds.get_sub_categories(category[0]+1).get("DATAGROUP_CODE")#gets the subcategory names for the main categories, though adding one leads to and error in folder stucture wrong data goes to wrong folder
			data_group_name = evds.get_sub_categories(category[0]+1).get("DATAGROUP_NAME")#gets the subcategory names,which will be the name of the subfolder,which will increase readbility
			pbar_sub_category = tqdm.tqdm(desc="Sub-Category",total=data_group_code.shape[0],leave=True)#Progress bar
			for i,sub_category in enumerate(data_group_code):#iterate subcategories to get the series
				os.chdir(folder_main)
				folder_sub = Path(Path.cwd(),data_group_name[i])#form the subfolder under the main category folder
				if not os.path.exists(folder_sub):
					os.mkdir(folder_sub)
				pbar_sub_category.update(1)


				pbar_series = tqdm.tqdm(desc="Series",total=evds.get_series(sub_category).values.shape[0],leave=False)#Progress bar
				for value in evds.get_series(sub_category).values:#iterate the series, value is of type tuple
					serie_code = value[0]
					start_date = value[2]
					file_name = value[1]
					file_name = remove_illegal_characters(file_name)#dosya adlarında izin verilmeyen karakterlerin silinmesi
					end_date = datetime.date.today().strftime("%d-%m-%Y")#end date needs to be in format dd-mm-yyyy
					try:
						os.chdir(folder_sub)
						if not os.path.exists(file_name + ".xlsx"):
							df = evds.get_data([serie_code],startdate=start_date,enddate=end_date,formulas=list(formul))#Server geç cevap verdiğinde 10 sn bekleyip devam ediyoruz
							df.to_excel(file_name + ".xlsx")  # instead of excel write to db
					except Exception as e:
						if str(e).__contains__("Read timed out."):
							time.sleep(10)
							df = evds.get_data([serie_code],startdate=start_date,enddate=end_date,formulas=formul)
							df.to_excel(file_name + ".xlsx")
							continue
						if str(e).__contains__("No such file or directory"):#Couldn't understand why this error occurs
							time.sleep(10)
							df = evds.get_data([serie_code],startdate=start_date,enddate=end_date)
							df.to_excel(file_name + ".xlsx")
							continue
						continue

					pbar_series.update(1)#Progress bar

				pbar_series.close()#Progress bar
			pbar_sub_category.close()#Progress bar
			pbar_main.update(1)#Progress bar
		except Exception as e:
			print(e)



def install_requirements(filename) -> None:
	with open(filename, 'r') as file:
		requirements = file.readlines()
	pbar = tqdm.tqdm(desc="Progress",total=len(requirements))
	for requirement in requirements:
		requirement = requirement.strip()
		if requirement:
			subprocess.call(['py', '-m', 'pip', 'install', "-q","-q","-q", requirement])
		pbar.update(1)



def main(api_key) -> None:
	evds = evdsAPI(api_key)
	main_directory = Path(Path.cwd(), "EVDS_Excel_Dosyaları")
	if not os.path.exists(main_directory):
		os.mkdir(main_directory)
	write_to_db(evds)
	#get_macro_info(evds, main_directory)
	#read_data()

if __name__ == "__main__":
	"""
	print("              \n\t\t\t****TCMB EVDS Data Collector****\n             ")
	print("This tool collects data using Python API of the EVDS system of TCMB, which consist of macroeconomic data")
	print("\nTo use the API you need to have an API key, which you can acquire by signing up to TCMB website.")
	print("\nData is structured as Main Category -> Sub-Category -> Serie progress bars follows the same structure")
	print("\nChecking the required libraries\n")
	requirements_file = "requirements.txt"
	install_requirements(requirements_file)
	print("\nRequired Libraries installed.\n")
	"""
	print("\nPlease enter the API Key you acquired")
	api_key = input("\nAPI-Key:")
	main(str(api_key))



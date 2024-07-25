#Work in Progress!!
from evds import evdsAPI
import pandas
from pathlib import Path
from datetime import date
import os


evds = evdsAPI("8lqJtipjux")

main_directory = Path(Path.cwd(),"EVDS_Excel_Dosyaları")
for category in evds.main_categories.iterrows():#start to iterate every main category
	try:
		os.chdir(main_directory)#make the cwd main directory
		folder_main = Path(Path.cwd(),category[1].array[1])#get the main category name and create the folder for the main category
		os.mkdir(folder_main)#Ana kategori adı ile cwd de bir klasör oluşturuyor
		data_group_code = evds.get_sub_categories(category[0]+1).get("DATAGROUP_CODE")#gets the subcategory names for the main categories, though adding one leads to and error in folder stucture wrong data goes to wrong folder
		for serie in data_group_code:#iterate subcategories to get the series
			os.chdir(folder_main)
			folder_sub = Path(Path.cwd(),serie)#form the subfolder under the main category folder
			os.mkdir(folder_sub)
			for value in evds.get_series(serie).values:#iterate the series, value is of type tuple
				serie_code = value[0]
				start_date = value[2]
				file_name = value[1]
				end_date = str(date.today().day)+"-"+"0"+str(date.today().month)+"-"+str(date.today().year)#end date needs to be in format dd-mm-yyyy
				df = evds.get_data([serie_code],startdate=start_date,enddate=end_date)
				os.chdir(folder_sub)
				df.to_excel(file_name+".xlsx")

	except Exception as e:#Have to handle Read timed out exception, although this is an exception it doesn't stop the program execution
		print(e)# When above exception is thrown program stops reading the current series and jumps on to the next main category

"""
Error Log: #these errors don't stop the program execution but lead to incomplete and false data or false folder structure

HTTPSConnectionPool(host='evds2.tcmb.gov.tr', port=443): Read timed out. (read timeout=None)
HTTPSConnectionPool(host='evds2.tcmb.gov.tr', port=443): Read timed out. (read timeout=None)
Cannot save file into a non-existent directory: 'A31.1.Vadesiz Mevduat'
HTTPSConnectionPool(host='evds2.tcmb.gov.tr', port=443): Read timed out. (read timeout=None)
[Errno 2] No such file or directory: '1:TÜRKİYE BRÜT DIŞ BORÇ STOKU.xlsx'
Category not found.
[Errno 22] Invalid argument: 'SİGORTA TEKNİK REZERVLERİ(**) (Bin TL).xlsx'
[Errno 2] No such file or directory: '(Genel Olarak)_ Geçen üç ayda, işletmelerle ilgili kredilerin ve kredi limitlerinin onaylanmasında uygulanan Bankanız kredi standartları ne yönde değişti?.xlsx'
[Errno 22] Invalid argument: 'TOPLAM(*) (Bin TL).xlsx'
HTTPSConnectionPool(host='evds2.tcmb.gov.tr', port=443): Read timed out. (read timeout=None)
HTTPSConnectionPool(host='evds2.tcmb.gov.tr', port=443): Read timed out. (read timeout=None)
[Errno 22] Invalid argument: '8.(KISITLAYAN FAKTÖR YOKTUR) Şu anda hangi faktör(ler) üretiminizi kısıtlamaktadır? (Yüzde pay).xlsx'
Category not found.
HTTPSConnectionPool(host='evds2.tcmb.gov.tr', port=443): Read timed out. (read timeout=None)
HTTPSConnectionPool(host='evds2.tcmb.gov.tr', port=443): Read timed out. (read timeout=None)
Cannot save file into a non-existent directory: 'İşletme'
[Errno 22] Invalid argument: '1. Ödeme Mesaj Adedi*.xlsx'
Cannot save file into a non-existent directory: 'Arjantin _ Kredi'
Cannot save file into a non-existent directory: 'Cumhuriyet Altını Satış Fiyatı (TL'
Cannot save file into a non-existent directory: 'Türkiye Konut Birim Fiyatları _ TL'

"""
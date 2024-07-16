#Work in Progress!!
from evds import evdsAPI
import pandas
from pathlib import Path

evds = evdsAPI("8lqJtipjux")

categories = evds.main_categories
print(type(categories))

print(categories.to_string()+"\n")

for category in evds.main_categories.iterrows():
	for sub_category in category:# Tüm kategorileri itere ederek, alt kategorilere ulaşmak için for döngüsü
		#daha her alt kategori altında bulunan verileri(örneğin TP.EUR.MT01 gibi) excel olarak kaydedicez



print("\n"+evds.get_sub_categories(3).to_string())
print("\n"+evds.get_series("TP.EUR.MT01").to_string())
print("\n")

#excel_file = evds.get_data(series=["FİYAT ENDEKSLERİ"],startdate="04-01-2002",enddate="16-07-2024").to_excel(excel_writer="output.xlsx",sheet_name="sheet1")

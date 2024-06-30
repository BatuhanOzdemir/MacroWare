from bs4 import BeautifulSoup
from urllib.request import urlopen
import xlsxwriter

#01.06.2024 itibariyle
son_bildirim_sayısı = 1293434

row = 0
column = 0
sheet = 0

workbook = xlsxwriter.workbook.Workbook("Kap_linkleri.xlsx")
worksheet = workbook.add_worksheet(str(sheet))

#kap.org'daki bütün bildirim linklerini bir excel dosyasına yazıdırıyor
#85084 ile başlıyor kap bildirimleri bundan önceki sayılar yok
#excel dosyasındaki her çalışma sayfası 65530 link alabiliyor, bu yüzden her 65530'uncu linkte yeni bir çalışma sayfası açılıyor

for i in range(85084,son_bildirim_sayısı):
	url = "https://www.kap.org.tr/tr/Bildirim/"+str(i)
	worksheet.write(row,column,url)
	row += 1
	if i % 65530 == 0:
		sheet += 1
		worksheet = workbook.add_worksheet(str(sheet))
		row = 0

workbook.close()


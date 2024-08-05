#Work in Progress!!
import time
from evds import evdsAPI
import subprocess
from pathlib import Path
from datetime import date
import os




def remove_illegal_characters(filename) -> str:
	#illegal_characters = ["<", ">", ":", "/", "\\", "|", "?"]
	allowed_filename = "".join(ch for ch in filename if ch.isalnum())
	return allowed_filename


def loading(iteration, total ,prefix="",suffix="",decimals=1,length=100,fill=">"):
	percent = ('{0:.' + str(decimals) +'f}').format(100*(iteration/float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + "-" * (length - filledLength)
	print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="\r")
	if iteration == total:
		print()


def get_macro_info(evds,main_directory) -> None:
	current_iteration = 0 #To count iteration of the progress bar
	iter_sub_group = 0
	iter_serie = 0
	print("\n\nProgress on the main categories\n")
	print("\nBeware the process is quite long!\n\n")
	loading(current_iteration, evds.main_categories.shape[0], prefix="Main Category", suffix="Complete\n", length=50)
	print("\n")
	for category in evds.main_categories.iterrows():#start to iterate every main category
		try:
			os.chdir(main_directory)#make the cwd main directory
			folder_main = Path(Path.cwd(),category[1].array[1])#get the main category name and create the folder for the main category
			if not os.path.exists(folder_main):
				os.mkdir(folder_main)#Ana kategori adı ile cwd de bir klasör oluşturuyor
			data_group_code = evds.get_sub_categories(category[0]+1).get("DATAGROUP_CODE")#gets the subcategory names for the main categories, though adding one leads to and error in folder stucture wrong data goes to wrong folder
			iter_sub_group = 0
			loading(current_iteration, data_group_code.shape[0], prefix="Sub-Category", suffix="Complete", length=50)
			print("\n")
			for serie in data_group_code:#iterate subcategories to get the series
				os.chdir(folder_main)
				folder_sub = Path(Path.cwd(),serie)#form the subfolder under the main category folder
				if not os.path.exists(folder_sub):
					os.mkdir(folder_sub)
				iter_sub_group += 1
				loading(iter_sub_group, data_group_code.shape[0], prefix="Sub-Category", suffix="Complete", length=50)
				iter_serie = 0
				loading(iter_serie, evds.get_series(serie).values.shape[0], prefix="Serie", suffix="Complete", length=50)
				print("\n")
				for value in evds.get_series(serie).values:#iterate the series, value is of type tuple
					serie_code = value[0]
					start_date = value[2]
					file_name = value[1]
					file_name = remove_illegal_characters(file_name)#dosya adlarında izin verilmeyen karakterlerin silinmesi
					end_date = str(date.today().day)+"-"+"0"+str(date.today().month)+"-"+str(date.today().year)#end date needs to be in format dd-mm-yyyy
					try:
						df = evds.get_data([serie_code],startdate=start_date,enddate=end_date)#Server geç cevap verdiğinde 10 sn bekleyip devam ediyoruz
					except Exception as e:
						if str(e).__contains__("Read timed out."):
							time.sleep(10)
							df = evds.get_data([serie_code],startdate=start_date,enddate=end_date)

					os.chdir(folder_sub)
					if not os.path.exists(file_name+".xlsx"):
						df.to_excel(file_name+".xlsx")
					iter_serie += 1
					loading(iter_serie, evds.get_series(serie).values.shape[0], prefix="Serie", suffix="Complete", length=50)

		except Exception as e:#Have to handle Read timed out exception, although this is an exception it doesn't stop the program execution
			print(e)
		current_iteration += 1
		loading(current_iteration, evds.main_categories.shape[0], prefix="Main Category", suffix="Complete", length=50)

def install_requirements(filename) -> None:
	with open(filename, 'r') as file:
		requirements = file.readlines()
	current_iteration = 0
	loading(current_iteration, len(requirements), prefix="Progress", suffix="Complete", length=50)
	for requirement in requirements:
		requirement = requirement.strip()
		if requirement:
			subprocess.call(['py', '-m', 'pip', 'install', "-q","-q","-q", requirement])
		current_iteration += 1
		loading(current_iteration, len(requirements), prefix="Progress", suffix="Complete", length=50)

def main(api_key) -> None:
	evds = evdsAPI(api_key)
	main_directory = Path(Path.cwd(), "EVDS_Excel_Dosyaları")
	if not os.path.exists(main_directory):
		os.mkdir(main_directory)
	get_macro_info(evds, main_directory)

if __name__ == "__main__":

	print("              \n\t\t\t****TCMB EVDS Data Collector****\n             ")
	print("This tool collects data using Python API of the EVDS system of TCMB, which consist of macroeconomic data")
	print("\nTo use the API you need to have an API key, which you can acquire by signing up to TCMB website.")
	print("\nData is structured as Main Category -> Sub-Category -> Serie progress bars follows the same structure")
	print("\nChecking the required libraries\n")
	requirements_file = "requirements.txt"
	install_requirements(requirements_file)
	print("\nRequired Libraries installed.\n")
	print("\nPlease enter the API Key you acquired")
	api_key = input("\nAPI-Key:")
	main(str(api_key))



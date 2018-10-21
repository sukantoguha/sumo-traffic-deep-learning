from bs4 import BeautifulSoup
import os
import datetime
def results():
	in_file = open("tripinfo.xml","r")
	contents = in_file.read()
	soup = BeautifulSoup(contents,'xml')
	one_car = soup.find_all('tripinfo')
	count_cars =0
	timeLoss_count=0
	for values in one_car:
		try:
			timeLoss = round(float(values['timeLoss'])*float(values['timeLoss']),5)
		except:
			continue
		timeLoss_count = timeLoss_count+ timeLoss
		count_cars = count_cars+1
	if count_cars !=0:
		if os.path.exists("results.txt"):
			a_w = 'a'
		else:
			a_w='w'
		#change output file here
		print("writing to the results.txt file")
		#fp = open("results_"+str(datetime.datetime.now().time())+".txt",a_w)
		fp = open("results_1.txt",a_w)
		fp.write(str(round(timeLoss_count/count_cars,5)))
		fp.write("\n")

if __name__ == "__main__":
	results()



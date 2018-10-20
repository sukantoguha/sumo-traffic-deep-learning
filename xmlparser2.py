import xml.etree.ElementTree as ET
def results():
	tree = ET.parse('tripinfo.xml')
	root = tree.getroot()
	sumSq = 0
	dictTotal = []
	for child in root:
		dictTotal.append(child.attrib)
	for dict in dictTotal:
		sumSq += float(dict.get('timeLoss')) ** 2
	if dictTotal !=0:
		print(sumSq/len(dictTotal))

if __name__ == "__main__":
	results()

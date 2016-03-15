from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import re
import csv
import os
import shutil

# pdfminer API
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def output_data(content, file_name):
	# Load data into lists
	output_dates = re.findall(r'[0-9]{0,2}/[0-9]{0,2}/[0-9]{4} [0-9]{0,2}:[0-9]{2}:[0-9]{2} [A-P][M]', content)
	output_temps = re.findall(r'[0-9]*\.[0-9]', content)

	length = len(output_dates)

	# Print data into consol
	# i = 0
	# while i < length:
	# 	print output_dates[i],"|", output_temps[i]
	# 	i += 1

	# Write data into csv file
	with open(file_name, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["Date & Time", "Temperature (F)"])
		writer.writerow([])
		i = 0
		while i < length:
			writer.writerow([output_dates[i], output_temps[i]])
			i += 1
	

	# Write Data into txt file
	# i = 0
	# with open(file_name, 'w') as txtfile:
	# 	while i < length:
	# 		txtfile.write(str(output_dates[i]) + " | " +str(output_temps[i])+"\n")
	# 		i += 1

# orient script to proper directory
print "Building directory structure..."
directory = os.getcwd()
os.chdir('..')

# # Get all files from directories
files = os.listdir(directory)
os.chdir(directory)
os.mkdir('data')
os.mkdir('csv')
# Move pdfs into data directory
for i in files:
	if i == 'pdf2csv.py' or i == '.DS_Store':
		pass
	else:
		shutil.move(i, 'data/'+i)

# Run script through all data in directory
print "-------------------------------------"
print os.getcwd()

# Assign pdf_files to pdf file names
pdf_files = os.listdir('data')

# Listing pdf files
for x in pdf_files:
	print x
print "-------------------------------------"

# Switch back to data file
os.chdir('data')
print "-------------------------------------"
print os.getcwd()

# content = convert_pdf_to_txt("US Fooods Freezer 11.12.12.pdf")
# print content

# Extracting information
for x in pdf_files:
	#print str(x)
	print os.getcwd()
	print "running pdf extraction"

	# pull data from pdf
	content = str(convert_pdf_to_txt(x))
	print content

	# export data to csv
	os.chdir('..')
	os.chdir('csv')
	output_data(content,x+str('.csv'))
	os.chdir('..')
	os.chdir('data')








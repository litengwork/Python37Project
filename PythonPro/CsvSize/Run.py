import glob
import os

src = '/Users/liteng/Desktop/WEWCFile/07.KUMEJIMA-csv/*.txt'

list = glob.glob(src)
for file in list:
    filename = file.split('/')[len(file.split('/'))-1]
    fsize = os.path.getsize(file)
    fsize = fsize / float(1000 * 1000)
    print(filename + ":" + str(round(fsize,2)))
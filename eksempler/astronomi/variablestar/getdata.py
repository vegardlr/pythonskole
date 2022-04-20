import os,sys
import urllib.request
import numpy as np
import matplotlib.pyplot as plt


#url = "http://mizar.voksenlia.net/Variable/Redukvis/W-lyr/01-63-76/"
#url = "http://mizar.voksenlia.net/Variable/Redukvis/W-lyr/02-76-82/"
url = "http://mizar.voksenlia.net/Variable/Redukvis/W-lyr/03-82-89/"
url = "http://mizar.voksenlia.net/Variable/Redukvis/W-lyr/04-89-97/"
url = "http://mizar.voksenlia.net/Variable/Redukvis/W-lyr/05-97-03/"
url = "http://mizar.voksenlia.net/Variable/Redukvis/W-lyr/06-03-08/"
datafolder = "W-lyr"
if not os.path.isdir(datafolder):
    os.mkdir(datafolder)


def isdata(line):
    elements = str(line.decode('UTF8')).split(" ")
    #print(elements)
    if len(elements) < 4:
        return False
    try: 
        float(elements[1])
    except ValueError: 
        return False
    try: 
        float(elements[-1])
    except ValueError: 
        return False
    return True

def extractdata(line):
    elements = str(line.decode('UTF8')).split(" ")
    return [float(elements[1]),float(elements[-1])]


print("Downloading data from: "+url)
indexfile = datafolder+"/index.html"
#if not os.path.isfile(indexfile):
os.system("wget -O "+indexfile+" "+url)
index = open(indexfile)
data = []
for iline in index:
    if "MAG" in iline:
        magfile=iline[81:90]
        print("Reading data from: "+magfile)
        mf = urllib.request.urlopen(url+magfile)
        for mline in mf.readlines():
            line = mline.rstrip()
            if isdata(line):
                data.append(extractdata(line))

data = np.array(data)
datafile = datafolder+"/data.txt"

plt.plot(data[:,0],data[:,1])
plt.title("Preview of "+datafile)
plt.xlabel("JD")
plt.ylabel("Mag")
plt.show()


print("Writing data to: "+datafile)
if os.path.isfile(datafile):
    print("Datafile exists: "+datafile)
    mode=None
    while mode != "a" and mode != "w" and mode != "q":
        mode = input("Overwrite (w), append (a) or quit (q)? ")

if mode == "q":
    sys.exit(0)

with open(datafile,mode) as f:
    f.write("#Data source:"+url+"\n")
    f.write("#JD    MAG\n")
    for d in data:
        s = [str(i) for i in d]
        f.write("\t".join(s)+"\n")



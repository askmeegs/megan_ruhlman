import csv
import os
import pprint as pp

files = os.listdir('out/')

for fn in files[1:2]:
    with open('out/'+fn, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = dict((rows[0],rows[1]) for rows in reader)
        pp.pprint(mydict)

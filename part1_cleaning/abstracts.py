import csv

with open('sheetsabs.csv', 'r') as csvfile:
    rd = csv.reader(csvfile)
    abstracts = [row[0].decode('unicode_escape').encode('ascii','ignore') for row in rd]

print len(abstracts)
cleaned = []
for a in abstracts:
    #print "\n\n******cleaning ", a
    if a[0] == ('\"' or '\''):
        a = a[1:] #remove beginning quotations
    spl = a.split('.')
    actual = spl[:len(spl)-1] #go up to the last period, remove stuff after that
    u = ' '.join(actual)
    #print "\nnow at ", u
    #get rid of "research supported by"
    if '(Research' in u:
        u = u.split('(Research')
        u = u[:len(u)-1]
        u = ' '.join(u)
        u = u.strip()
        #print "\nnow at", u
    u = u + "."
    if u != '.': #check if nonempty
        cleaned.append(u)

print "# abstracts: ", len(cleaned)

with open('abstracts2.txt', 'wb') as outfile:
    for item in cleaned:
        outfile.write("%s\n" % item)

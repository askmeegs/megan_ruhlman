from collections import Counter
import csv
import string
import pprint

#make tokens
with open('abstracts1997.2015.txt') as infile:
    rawlines = infile.readlines()
    lines = [l.decode("utf8").lower().strip() for l in rawlines]

print lines[500:510]
lines = [l for l in lines if l != '']
exclude = set(string.punctuation)
temp = []
for l in lines:
    temp.append(''.join(ch for ch in l if ch not in exclude))
lines = temp

#filter stopwords -> tokenize
filtered = []
with open('stopwords.txt') as inf:
    sws = [s.strip() for s in inf.readlines()]

for l in lines:
    temp = []
    tokened = l.split(' ')
    for t in tokened:
        if t not in sws:
            temp.append(t)
    filtered.append(temp)

#make IDs and labels
flat = [item for sublist in filtered for item in sublist]
counts = Counter(flat).most_common(1000)
counts = counts[3:]

labeledCounts = zip(xrange(1,1001), counts)

#create dict mapping word to ID
labels = {}
for tup in labeledCounts:
    id = tup[0]
    word = tup[1][0]
    labels[word] = id

writer = csv.writer(open('labels.csv', 'wb'))
for key, value in labels.items():
   writer.writerow([unicode(key).encode("utf-8") , unicode(value).encode("utf-8")])

print "Getting weights..."
#now get the weights- words get weighted that occur in the same abstract
#{(sourceID, targetID): weight}
#calling labels[word] gets the ID
weights = {}
for i, tas in enumerate(filtered): #list of words
    if i%10 == 0:
        print "on abstract", i
    for sword in tas:
        if sword in labels: #labels only has the top 10000 + stopwords removed!
            sid = labels[sword]
            for tword in tas:
                if tword in labels:
                    tid = labels[tword]
                    if (sid != tid):  #don't weight a word with itself
                        if (sid, tid) in weights:
                            weights[(sid, tid)] = weights[(sid, tid)] + 1
                        else: #pair already in weights
                            weights[(sid, tid)] = 1

writer = csv.writer(open('weights.csv', 'wb'))
for key, value in weights.items():
    if value > 1:
        writer.writerow([unicode(key[0]).encode("utf-8") , unicode(key[1]).encode("utf-8"), unicode(value).encode("utf-8")])

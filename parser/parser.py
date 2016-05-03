import docx
from docx import Document
import os
import csv

#INDICES: 0- year, 1- title, 2-presenter, 3-advisor, 4on-abstract
def clean(para):
    year = para[0]
    title = para[1]
    presenter = para[2]
    advisor = para[3]
    abstract = ' '.join(para[4:])
    return [year, title, presenter, advisor, abstract]

def getOneYear(fn):
    projects = []
    year = fn.split("_")[3]
    f = open(fn)
    document = docx.Document(f)
    paragraphs = [p.text for p in document.paragraphs]
    for p in paragraphs:
        print p
    #try to parse the individual projects
    for i, p in enumerate(paragraphs):
        if 'advisor' in p.lower():
            para = [year, paragraphs[i-2], paragraphs[i-1], p]
            index = i+1 #init
            while index < len(paragraphs):
                if (paragraphs[index] == '') or ('advisor' in paragraphs[index].lower()):
                    break
                else:
                    para.append(paragraphs[index])
                    index = index+1
            #cleaning
            updatedPara = clean(para)
            #remove the last two paragraphs (name/title of the next one)
            projects.append(updatedPara)
    asd = {}
    for i, proj in enumerate(projects):
        asd[i+1] = proj
    #return asd

    print "\n"+year+": ", len(asd), " PROJECTS."

    outname = "out/Ruhlman"+year+".csv"
    writer = csv.writer(open(outname, 'wb'))
    for key, value in asd.items():
        value = [z.encode('utf-8') for z in value]
        writer.writerow([key, value[0], value[1], value[2], value[3], value[4:]])

def getAllYears(dirName):
    files = os.listdir(dirName)
    for fn in files[7:8]:
        getOneYear(dirName + '/' + fn)


#dirName = 'word/'

#two = getOneYear('word/WCA_Ruhlman_prog_2002_final.docx')

getAllYears('word/')

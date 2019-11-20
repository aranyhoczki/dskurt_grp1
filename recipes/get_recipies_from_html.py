
import time
import datetime
from recipe_scrapers import scrape_me
import json
import ndjson

RECPATTERN='href="https://www.allrecipes.com/recipe/'
def get_list_from_file(filename):
    ret = []
    print ("Getting:",filename)
    file = open(filename, "r")
    filetxt = file.read()
    pos = 1
    max = 100000
    while pos > 0:
        max -=1
        if max < 1:
            break

        pos = filetxt.find(RECPATTERN, pos)
        if pos < 0:
            continue
        pos2 = filetxt.find(" ", pos+len(RECPATTERN))
        ru = filetxt[pos+6:pos2-1]
        print("ru:",ru)
        ret += [ru] 
        pos = pos2      
    file.close() 
    return ret

filename = "hungarian.html"
cuisine="hungarian"

all_rec_url = get_list_from_file(filename)
all_rec_url = list(dict.fromkeys(all_rec_url))
print("Total rec in :", cuisine, len(all_rec_url))
outfile1 = open("url_%s.txt"%cuisine, "w")
for uu in all_rec_url:
    outfile1.write(uu)
    outfile1.write("\n")


receipts = []
i = 1
for uu in all_rec_url:
        print("Get %d/%d (%s)"%(len(all_rec_url), i, uu))
        i+=1
        scraper = scrape_me(uu)
        r = {}
        r["url"] = uu
        r["baseurl"] = "https://www.allrecipes.com/search/results/?wt=hungarian"
        r["cuisine"] = cuisine
        r["ingredients"] = scraper.ingredients()
        r["title"] = scraper.title()
        r["instructions"] = scraper.instructions()
        r["total_time"] = scraper.total_time()
        receipts += [r]
outfile = open("recipes_%s.ndjson"%cuisine, "w")
ndjson.dump(receipts, outfile)





        

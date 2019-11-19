
import wget
import time
import datetime
from recipe_scrapers import scrape_me
import json
import ndjson


cuisine_tuple = [("https://www.allrecipes.com/recipes/1470/world-cuisine/latin-american/mexican/authentic/", "mexican"),
                     ("https://www.allrecipes.com/recipes/721/world-cuisine/european/french/", "french"),
                     ("https://www.allrecipes.com/recipes/233/world-cuisine/asian/indian/", "indian"),
                     ("https://www.allrecipes.com/recipes/723/world-cuisine/european/italian/", "italian"),
                     ("https://www.allrecipes.com/recipes/702/world-cuisine/asian/thai/", "thai"),
                     ("https://www.allrecipes.com/recipes/695/world-cuisine/asian/chinese/", "chinese")]

cuisine_tuple1 = [("https://www.allrecipes.com/recipes/1470/world-cuisine/latin-american/mexican/authentic/", "mexican"),
                     ]

class Receipt:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=0)

RECPATTERN='href="https://www.allrecipes.com/recipe/'
def get_list_from_url(url):
    ret = []
    print ("Getting:",url)
    filename = wget.download(url)
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



for u in cuisine_tuple:
    all_rec_url = []
    for i in range(1,200):
        baseurl = u[0]+"?page=%d"%i
        try:
           all_rec_url += get_list_from_url(baseurl)
        except:
            break
    all_rec_url = list(dict.fromkeys(all_rec_url))
    print("Total rec in :", u[1], len(all_rec_url))
    i = 1
    receipts = []
    for uu in all_rec_url:
        print("Get %d/%d (%s)"%(len(all_rec_url), i, uu))
        i+=1
        scraper = scrape_me(uu)
        r = {}
        r["url"] = uu
        r["baseurl"] = u[0]
        r["cuisine"] = u[1]
        r["ingredients"] = scraper.ingredients()
        r["title"] = scraper.title()
        r["instructions"] = scraper.instructions()
        r["total_time"] = scraper.total_time()
        receipts += [r]
    outfile = open("recipes_%s.ndjson"%u[1], "w")
    ndjson.dump(receipts, outfile)





        

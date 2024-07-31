import requests as rq
import json
from bs4 import BeautifulSoup as bs

def lookAt(num):
    baseUrl = "https://ocen-piwo.pl/" 
    url = baseUrl + "katalog-piw-" # add number to the end (max 2347)
    raw = rq.get(url + str(num))
    soup = bs(raw.content, features="html.parser")

    main_div = soup.find("div",{"id":"main"})
    cont = main_div.find_all("fieldset")

    out = []

    for field in cont:
        name = field.find("legend").find("a")
        link = name['href']
        name = name.contents[0]

        table =  field.find("table")

        rawImg= table.find("img")
        try: img = rawImg["src"]
        except KeyError: img = rawImg["data-src"]


        tags = table.find("div", {"class":"tagsgroup"}).find_all("div",{"class":"tag"})
        alk = ""
        for tag in tags:
            if(len(tag.contents) >= 2):
                if "alk" in tag.contents[1]:
                    alk = tag.contents[1]

            
        alk = alk.replace(" ","").replace("alk.","").replace(",",".")

        rating = table.find("div",{"class":"news_com"}).find("span").find("span").contents[0] #+ "/10"
        rating = str(rating).replace(",",".")

        if rating[0] == '<': rating = -1
        if alk == '': alk = '0'

        #print(f"{name:70s} {(baseUrl + img):90s} {alk:20s} {rating:15s}")
        #print(f"{name:70s} {alk:20s} {rating:15s}")
        out.append({
            "name": name,
            "alk": float(alk),
            "rating": float(rating),
            "image": (baseUrl + img),
            "link": (baseUrl + link),
        })
    return out



def main():
    print("[STARTING DB_CREATION]")
    db = []
    num_max_beer_pages = 2625
    for i in range(num_max_beer_pages):
        print(f"DB-BLOCK[{i}/{num_max_beer_pages}] <-- writing", end="")
        try: 
            db += lookAt(i * 10)
            print(" [SUCCES]")
        except:
            print(" [FAILED]")
            continue 

    sdb = sorted(db, key=lambda x: x['alk']/100 * x["rating"])
    print("[DB SORTED]")

    with open("db.json", "w") as f:
        print("[DB FILE OPENED]")
        json.dump(sdb, f, indent=4)
        print("[FILE WRITTEN]")
        f.close()


    return 1

if __name__ == "__main__":
    main()




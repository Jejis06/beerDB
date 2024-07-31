import json
import random


def main():
    with open("legacy-db.json") as f:
        db = f.read()


    db = json.loads(db)
    SIZE = len(db)
    while True:
        num = int(input("query n random beers (n): "))
        m = 2300

        for i in range(0,num):
            print(db[random.randint(0, SIZE)]['name'])

    

    return

if __name__ == '__main__':
    main()

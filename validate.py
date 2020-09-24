#!/usr/bin/python3 -u

import json
import os
import re

results = {"errors": [], "warnings": [], "meta": { "tractmeasures": {}}}

with open('config.json', encoding='utf-8') as config_json:
    config = json.load(config_json)

if not os.path.exists("secondary"):
    os.mkdir("secondary")
if not os.path.exists("output"):
    os.mkdir("output")

#make sure we have a valid .tsv file
if not os.path.exists(config["tractmeasure"]):
    results["errors"].append("no tractmeasure.tsv")    
else:
    with open(config["tractmeasure"]) as f:
        rows = f.readlines()

    #copy to secondary
    with open("secondary/tractmeasure.tsv", "w") as f:
        f.write("".join(rows))
        f.close()

    #copy to primary output
    with open("output/tractmeasure.tsv", "w") as f:
        f.write("".join(rows))
        f.close()

    #parse data and store it on meta
    header = rows.pop(0).split("\t")
    data = rows.pop(0).split("\t")
    for column in header:
        column = re.sub('[^A-Za-z0-9]+', '', column)
        results["meta"]["tractmeasures"][column] = data.pop(0).strip()

with open("product.json", "w") as fp:
    json.dump(results, fp)

print("done");

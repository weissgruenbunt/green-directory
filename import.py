import csv
import os
import yaml
import sys

def dir_entries(path):
    """
    Iterator over all data files in the cloned green directory
    """
    for root, dirs, files in os.walk(path):
        for fname in files:

            filepath = os.path.join(root, fname)
            if not filepath.endswith(".yaml"):
                continue

            with open(filepath, 'r', encoding="utf-8") as yamlfile:
                for doc in yaml.load_all(yamlfile):
                    yield doc

def read_csv(path):
    """Einlesen der CSV-Daten"""

    lv = {}
    kv = {}
    ov = {}

    with open(path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:

            state_key = row[0][1:3]
            district_key = row[0][1:6]
            city_key = row[0][1:8]
            kind = row[1]
            name = row[2]
            url = row[3]

            if url != '' and not url.startswith('http'):
                url = 'http://' + url

            if kind == "LV":
                #print("%s %s" % (state_key, name))
                lv[state_key] = {
                    'state': name,
                    'url': url,
                }
            elif kind == "KV":
                #print("%s-%s %s" % (state_key, district_key, name))
                kv[district_key] = {
                    'state': lv[state_key]["state"],
                    'district': name,
                    'url': url,
                }
            elif kind == "OV":
                #print("%s-%s-%s %s" % (state_key, district_key, city_key, name))
                ov[city_key] = {
                    'state': lv[state_key]["state"],
                    'district': kv[district_key]["district"],
                    'city': name,
                    'url': url,
                }

    return (kv, ov)

def strip(s, stateName):
    s = s.replace("-", "").replace("/", "").replace("(", "").replace(")", "")
    s = s.replace(" und ","")
    s = s.replace(" ", "")
    s = s.lower()
    s = s.replace("kreis", "").replace("stadt", "").replace("land", "")
    s = s.replace(stateName.lower(), "")
    return s

def matchKV(kv, dkv):
    '''
    returns true if kv can be found in dkv
    '''
    key = "%s/%s" % (kv['state'], kv['district'])
    if key in dkv:
        return dkv[key]
    
    # create reduced list
    statelist = []
    for _ ,v in dkv.items():
        if v["state"] == kv["state"]:
            statelist.append(v)
       
    # 1 - match by stripped name
    strippedName = strip(kv["district"], kv["state"])
    
    results = []
    for elem in statelist:
        strippedName2 = strip(elem["district"], elem["state"])
        if strippedName == strippedName2:
            results.append(elem)
    if results:
        return results
    
    # 2 - match by part
    name1 = kv["district"]
    for elem in statelist:
        name2 = elem["district"]
        if name1 in name2:
            results.append(elem)
        elif name2 in name1:
            results.append(elem)
    if results:
        return results

if __name__ == "__main__":

    # CSV-Daten zum Import einlesen
    ikv, iov = read_csv("./daten.csv")

    # Bestehendes Verzeichnis in Dicts laden
    dkv = {}
    dov = {}
    durls = set()

    for doc in dir_entries("data/countries/de"):
        if doc['level'] == "DE:KREISVERBAND":
            key = "%s/%s" % (doc['state'], doc['district'])
            dkv[key] = doc
        if doc['level'] == "DE:REGIONALVERBAND":
            doc['district'] = doc['region']
            key = "%s/%s" % (doc['state'], doc['district'])
            dkv[key] = doc
        if doc['level'] == "DE:ORTSVERBAND":
            key = "%s/%s/%s" % (doc['state'], doc['district'], doc['city'])
            dov[key] = doc
        if 'urls' in doc:
            for entry in doc['urls']:
                if entry['type'] == "WEBSITE":
                    durls.add(entry['url'])

    # KV abgleichen
    kv_new = 0
    for i in sorted(ikv.keys()):
        kv = ikv[i]
        matched = matchKV(kv, dkv)
        key = "%s/%s" % (kv['state'], kv['district'])
        
        if matched and key not in dkv:
            if len(matched) == 1:
                print("GLEICH:", kv["district"], "==", matched[0]["district"])
            else:
                print("GLEICH?", kv["district"], "==", [m["district"] for m in matched], file=sys.stderr)
        if not matched:
            print("%s - KV '%s' ist neu - %s" % (i, key, ikv[i]["url"]))
            kv_new += 1

    # OV abgleichen
    ov_new = 0
    for i in sorted(iov.keys()):
        ov = iov[i]
        key = "%s/%s/%s" % (ov['state'], ov['district'], ov['city'])
        if key in dov:
            continue
        if ov['url'] == '':
            continue
        if ov['url'] in durls:
            continue
        print("%s - OV %s %s ist neu" % (i, key, ov['url']))
        ov_new += 1

    print("%d KV sind neu" % kv_new)
    print("%d OV sind neu" % ov_new)

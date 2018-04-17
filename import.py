import csv
import os
import yaml

def dir_entries(path):
    """
    Iterator over all data files in the cloned green directory
    """
    for root, dirs, files in os.walk(path):
        for fname in files:

            filepath = os.path.join(root, fname)
            if not filepath.endswith(".yaml"):
                continue

            with open(filepath, 'r') as yamlfile:
                for doc in yaml.load_all(yamlfile):
                    yield doc

def read_csv(path):
    """Einlesen der CSV-Daten"""

    lv = {}
    kv = {}
    ov = {}

    with open(path, "r") as csvfile:
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
        key = "%s/%s" % (kv['state'], kv['district'])
        if key not in dkv:
            print("%s - KV '%s' ist neu" % (i, key))
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

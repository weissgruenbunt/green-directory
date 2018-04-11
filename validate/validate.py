import os

from pykwalify.core import Core
import json
import sys
import yaml


schemaFile = "validate/schema.yaml"

doc_unique_keys = set()
emails = set()
urls = set()

def main():
    for root, _, files in os.walk("./data"):
        for f in files:
            path = os.path.join(root, f)
            checkFile(path)

def unique_doc_key(doc):
    """
    Derives a key allowing for uniqueness check
    from a document
    """
    keyparts = [doc['type']]

    for attr in ('level', 'country', 'state', 'region', 'district', 'city'):
        if attr in doc:
            keyparts.append(doc[attr])

    key = json.dumps(keyparts)
    return key

def checkFile(path):
    """
    Validate one file
    """
    with open(path, 'r') as yamlfile:
        contents = yaml.load_all(yamlfile)
        for i, doc in enumerate(contents):
            c = Core(source_data=doc, schema_files=[schemaFile])

            try:
                c.validate(raise_exception=True)
            except Exception as e:
                print("Schema validation error in {} entry {}".format(path, i))
                raise e
                sys.exit(1)

            # validate uniqueness
            key = unique_doc_key(doc)
            if key in doc_unique_keys:
                raise Exception("Entry is duplicate: {path} {key}".format(
                    path=path,
                    key=key
                ))
            doc_unique_keys.add(key)

            if 'emails' in doc:
                for address in doc['emails']:
                    if address['address'] in emails:
                        raise Exception("Email is duplicate: {email} {path} {key}".format(
                            email=address['address'],
                            path=path,
                            key=key
                        ))
                    emails.add(address['address'])

            if 'urls' in doc:
                for url in doc['urls']:
                    if url['url'] in urls:
                        raise Exception("URL is duplicate: {url} {path} {key}".format(
                            url=url['url'],
                            path=path,
                            key=key
                        ))
                    emails.add(url['url'])


if __name__== "__main__":
    main()

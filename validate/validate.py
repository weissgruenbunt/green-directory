import os

from jsonschema import validate
import json
import sys
import yaml

# Folder to contain our JSON schema
schema_folder = "schema"

# Folder containing our data
data_folder = "data"

# Dicts which we will use to detect uniqueness across the entire database
doc_unique_keys = set()
emails = set()
urls = set()

# Will hold our JSON schemas
schemas = {}


def main():
    # load schemas
    for root, _, files in os.walk(schema_folder):
        for f in files:
            # Expecting <typename>.json as file name
            (typename, _) = f.split('.')
            path = os.path.join(root, f)
            with open(path, 'r') as jsonfile:
                schema = json.load(jsonfile)
                schemas[typename] = schema

    # Walk through data for validation
    for root, _, files in os.walk(data_folder):
        for f in files:
            path = os.path.join(root, f)
            check_file(path, schemas)


def unique_doc_key(doc):
    """
    Creates a key that allows to check for record uniqueness
    """
    keyparts = [doc['type']]

    for attr in ('level', 'country', 'state', 'region', 'district', 'city'):
        if attr in doc:
            keyparts.append(doc[attr])

    key = json.dumps(keyparts)
    return key


def validate_entry_schema(entry, schemas):
    """
    Validate one record against the specific JSON schema.
    Raises a ValidationError is not valid.
    """
    validate(entry, schemas[entry['type'].lower()])


def check_file(path, schemas):
    """
    Validate all documents in a YAML file against our schemas
    """
    with open(path, 'r') as yamlfile:
        contents = yaml.load_all(yamlfile, yaml.SafeLoader)

        for i, doc in enumerate(contents):

            try:
                validate_entry_schema(doc, schemas)
            except Exception as e:
                print("Schema validation error in {} entry {}".format(path, i))
                raise e

            # validate uniqueness
            key = unique_doc_key(doc)
            if key in doc_unique_keys:
                raise Exception("Entry {index} is duplicate: {path} {key}".format(
                    index=i,
                    path=path,
                    key=key
                ))
            doc_unique_keys.add(key)

            if 'emails' in doc:
                for address in doc['emails']:
                    if 'address' not in address:
                        raise Exception("'emails' entry {index} has no 'address' attribute. Path: {path}".format(
                            index=i,
                            path=path,
                        ))
                    if address['address'] in emails:
                        raise Exception("Email in entry {index} is duplicate: {email} {path} {key}".format(
                            index=i,
                            email=address['address'],
                            path=path,
                            key=key
                        ))
                    emails.add(address['address'])

            if 'urls' in doc:
                for url in doc['urls']:
                    if 'url' not in url:
                        raise Exception("'urls' entry {index} has no 'url' attribute. Path: {path}".format(
                            index=i,
                            path=path,
                        ))
                    if url['url'] in urls:
                        raise Exception("URL in entry {index} is duplicate: {url} {path} {key}".format(
                            index=i,
                            url=url['url'],
                            path=path,
                            key=key
                        ))
                    urls.add(url['url'])


if __name__== "__main__":
    main()

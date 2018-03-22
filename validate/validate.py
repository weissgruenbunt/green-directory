import os

from pykwalify.core import Core
import yaml


schemaFile = "validate/schema.yaml"

def main():
    for root, _, files in os.walk("./data"):
        for f in files:
            path = os.path.join(root, f)
            checkFile(path)


def checkFile(path):
    with open(path, 'r') as yamlfile:
        contents = yaml.load_all(yamlfile)
        for i, doc in enumerate(contents):
            c = Core(source_data=doc, schema_files=[schemaFile])

            print("{} ({})".format(path, i))
            c.validate(raise_exception=True)


if __name__== "__main__":
    main()

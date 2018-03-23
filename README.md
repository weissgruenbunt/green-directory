# Green Directory

Structured data repository of Green Party organisations

## Goals

- Enable applications in need of structured data regarding
  Green party organizations

- Provide high quality, well maintained structured data

- Allow for an open and transparent data maintenance workflow
  based on Github pull requests.

## Status

This project is in a very early stage. We are currently exploring
how a schema could look for the data we want to store, with a focus
initially on Germany.

So far, only example records can be found here.

Expect the schema to change any time.

## Help Wanted

This project needs help with:

- Structured data imports: As soon as a schema is defined initially,
  we need help with importing data. Pull requests welcome!

Please also look at the [issues](https://github.com/netzbegruenung/green-directory/issues)
for anything tagged with `help wanted`.

When in doubt, please file an issue to ask a question or report
a feature wish.

## Data Structure

- YAML is used as a source format.

- We try to avoid as much extra markup as possible (quotes, brackets)

- We have a folder structure that helps humans to find relevant files,
  but which should not be read in a semantical fashion. The folder hierarchy
  can vary from country to country and from locality to locality.
  Likewise, data file names have no meaning.

- YAML files have the ending `.yaml`.

- All data files are lists of entries (starting with a `---` line).

- The schema definition (attributes and permitted values) depends on the
  type of entry. See below for details.

## Attributes

If not indicated otherwise, all attributes are of the type `String`.

- `type`: Type of the entry. Possible values:
  - `PARTY`: A political party, usually active in the entire country.
  - `REGIONAL_CHAPTER` - a subdivision of an organisation, usually
    assigned to a local territory.
  - `COMMITTEE`: A not locally assigned sub-group of a party
    organisation.

- `level` (mandatory). A sub-classification of an entry with type `REGIONAL_CHAPTER`. Possible values:
  - `DE:LANDESVERBAND`: A chapter belonging to a federal state in Germany. The
    "Land" (also known as "Bundesland") is the primary territorial subdivision
    of the Federal Republic of Germany. See https://en.wikipedia.org/wiki/States_of_Germany
  - `DE:KREISVERBAND`: A "Kreisverband" in Germany (DE), which is a regional
    chapter of the party belonging to a "Kreis", which is a kind of district.
    A "Kreis" is, in most German federal states, the primary adinistrative
    subdivision. See https://en.wikipedia.org/wiki/Districts_of_Germany
  - `DE:BEZIRKSVERBAND`: TODO
  - `DE:ORTSVERBAND`: TODO

TODO: To be continued. Please refer to examples in `data` for now.


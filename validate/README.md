# Validation

This folder contains schema definitions and tooling required for validation of
data contained in this repository.

The script `validate.py` is automatically run for every push to a branch or
pull request. It can also be executed locally. Simply run this from the
repo's root directory:

```
make validate
```

If you don't see any errors, the data is valid according to the schema in
the `schema.yaml` file.

You can find out more about the schema definition in the
[pykwalify documentation](http://pykwalify.readthedocs.io/en/unstable/validation-rules.html).

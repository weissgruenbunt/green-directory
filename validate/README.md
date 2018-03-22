# Validation

This folder contains definitions and tooling required for validation of data
contained in this repository.

The script `validate.py` is automatically run for every push to a branch or
pull request. It can also be executed locally. Synopsis:

```
pip install pykwalify
python ./validate/validate.py
```

If you don't see any output, the data is valid according to the schema in
the `schema.yaml` file.

You can find out more about the schema definition in the
[pykwalify documentation](http://pykwalify.readthedocs.io/en/unstable/validation-rules.html).

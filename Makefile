
.PHONY: validate

venv:
	virtualenv -p python3 venv
	venv/bin/pip install yamllint pykwalify

validate: venv
	venv/bin/yamllint -d "{extends: default, rules: {line-length: {max: 120}}}" ./data
	venv/bin/yamllint ./validate/schema.yaml
	venv/bin/python ./validate/validate.py

install:
	pip install -r requirements.txt

spec:
	python -m unittest -b

env:
	virtualenv -p python3 env

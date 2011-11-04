# Installation #

You must have [xerox](https://github.com/kennethreitz/xerox) and [bitly-api-python](https://github.com/bitly/bitly-api-python) installed for this program to run.

Simply copy config.py.example to config.py and edit in your username and password!

# Example setup #
	pip install xerox
	pip install -e git://github.com/bitly/bitly-api-python.git#egg=bitly_api

	cp config.py.example config.py
	vim config.py
	python ./bitcpy.py

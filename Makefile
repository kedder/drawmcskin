all: ve

ve: 
	virtualenv -p python3 ve
	ve/bin/pip install -r requirements.txt
	ve/bin/pip install -e .
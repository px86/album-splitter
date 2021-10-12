LOG = log.txt

all: test

test: albumsplit.py examples/demo.opus examples/demo.csv
	python albumsplit.py examples/demo.opus examples/demo.csv --log $(LOG) 

clean:
	rm -f $(LOG)

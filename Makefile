all: setup run

setup:
	pip3 install tk

run:
	python3 fireshark.py

clean:
	rm -r __pycache__/

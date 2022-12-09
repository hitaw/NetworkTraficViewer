all: setup run

setup:
	python3 get-pip.py | pip3 install tk

run:
	python fireshark.py

clean:
	rm -r __pycache__/

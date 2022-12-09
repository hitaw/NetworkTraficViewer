all: setup run

setup:
	brew install python3 | brew postinstall python3 | pip3 install tk

run:
	python fireshark.py

clean:
	rm -r __pycache__/


all: setup run
	
setup:
	python -m ensurepip --upgrade | python -m pip install tk

run:
	python fireshark.py

clean:
	rm -r __pycache__/

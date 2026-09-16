.PHONY: run test

run:
	python3 -m src.demo_server

test:
	python3 -m unittest discover -s tests -v
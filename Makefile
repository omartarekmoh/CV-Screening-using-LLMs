ENV_NAME=mini-rag-app

run:
	./run.sh

test:
	pytest

lint:
	flake8 src/

format:
	black src/

install:
	pip install -r src/requirements.txt

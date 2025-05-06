run:
	./shells/run.sh

test:
	pytest

lint:
	flake8 src/

format:
	black src/

install:
	./shells/install.sh

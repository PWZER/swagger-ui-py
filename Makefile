format:
	@python3 -m pip install --disable-pip-version-check --no-cache-dir autopep8 isort flake8
	@autopep8 --recursive --max-line-length 100 --in-place --ignore-local-config .
	@isort --line-width=100 --force-single-line-imports .

format-check:
	@python3 -m pip install --disable-pip-version-check --no-cache-dir autopep8 isort flake8
	@autopep8 --recursive --max-line-length 100 --diff --ignore-local-config .
	@isort --line-width=100 --force-single-line-imports --check .

build:
	@rm -rf ./dist/*
	@python3 setup.py bdist_wheel

install: build
	@python3 -m pip uninstall -y swagger-ui-py > /dev/null 2>/dev/null
	@python3 -m pip install --disable-pip-version-check --no-cache-dir -r test/requirements.txt
	@python3 -m pip install --disable-pip-version-check --no-cache-dir dist/swagger_ui_py-*.whl

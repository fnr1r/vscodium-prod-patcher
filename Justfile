SRC_DIR := "src/vscodium_prod_patcher"

build:
    python -m build --wheel --no-isolation

clean:
    -rm -r dist

clean-all: clean clean-pycache

clean-pycache:
    -find {{SRC_DIR}} -iname __pycache__ -exec rm -r {} +

check: mypy pylint flake8

alias fmt := flake8
alias flake := flake8
alias lint := pylint
alias typecheck := mypy

flake8:
    -uv run flake8 {{SRC_DIR}}

isort:
    -uv run isort {{SRC_DIR}}

mypy:
    -uv run mypy {{SRC_DIR}} --check-untyped-defs

pylint:
    -uv run pylint {{SRC_DIR}} --disable C0114,C0115,C0116

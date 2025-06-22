DIST_DIR := "dist"
SRC_DIR := "src"

build:
    python -m build --wheel --no-isolation \
        --outdir {{DIST_DIR}}
    python -m build --wheel --no-isolation \
        --outdir {{DIST_DIR}} \
        src/vscodium_prod_patcher_alpm_ini

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
    -uv run mypy {{SRC_DIR}}

pylint:
    -uv run pylint \
        --disable C0114,C0115,C0116 \
        --extension-pkg-allow-list pyalpm \
        {{SRC_DIR}}

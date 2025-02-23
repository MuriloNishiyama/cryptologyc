#!/bin/bash
set -e 

install_curl() {
    echo "curl not found. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y curl
    elif command -v brew &> /dev/null; then
        brew install curl
    else
        echo "I could not install CURL. You will have to install manually."
        exit 1
    fi
}

if ! command -v curl &> /dev/null; then
    install_curl
else
    echo "curl already installed."
fi

if ! command -v duckdb &> /dev/null; then
    echo "duckdb not found. Installing duckdb..."
    curl https://install.duckdb.org | sh # https://duckdb.org/docs/installation/index?version=stable&environment=cli&platform=linux&download_method=direct&architecture=x86_64
else
    echo "duckdb already installed."
fi

if [ ! -d "data" ]; then
    echo "Creating 'data'..."
    mkdir data
fi

DB_PATH="data/cryptologyc.duckdb"

if [ ! -f "$DB_PATH" ]; then
    echo "Creating database DuckDB: cryptologyc..."
    duckdb "$DB_PATH" <<EOF
.exit
EOF
else
    echo "DuckDB 'cryptologyc' already exists."
fi

echo "Configuration completed"

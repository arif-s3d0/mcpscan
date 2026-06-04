# mcpscan

A small client for enumerating and interacting with FastMCP servers.

## Setup venv
python -m venv venv

## Install
pip install -r requirements.txt

## Usage
List everything (default):
    python mcpscan.py --host 172.17.0.2:8000

Read a resource:
    python mcpscan.py --host HOST --resource "resource://items"

Call a tool:
    python mcpscan.py --host HOST --tool execute_server_command command=date

URL-encode spaces in resource/tool params:
    python mcpscan.py --host HOST --encode --resource "price://x' UNION SELECT ..."

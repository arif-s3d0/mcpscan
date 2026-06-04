# mcpscan

A small client for enumerating and interacting with FastMCP servers.

### Setup venv
```bash
python -m venv venv
```

### Install
```bash
pip install -r requirements.txt
```

### Usage

List everything:

```bash
python mcpscan.py --host 172.17.0.2:8000
```

Read a resource:

```bash
python mcpscan.py --host HOST --resource "resource://items"
```

Call a tool:

```bash
python mcpscan.py --host HOST --tool execute_server_command command=date
```

URL-encode spaces in resource/tool params:

```bash
python mcpscan.py --host HOST --encode --resource "price://x' UNION SELECT SELECT sqlite_version()-- -"  
```

<img width="1531" height="129" alt="image" src="https://github.com/user-attachments/assets/20f229ee-f5a4-42c3-959d-04ce1cb21672" />

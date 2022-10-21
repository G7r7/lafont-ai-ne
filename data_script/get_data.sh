#!/bin/bash

pip install -r requirements.txt

python3 create_db_file.py
python3 get_french_poetry_utf8.py

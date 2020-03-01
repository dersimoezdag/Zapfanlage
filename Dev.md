# Requirements generieren:

py -3.7-64 -m pip install -r requirements.txt

# Update Strings:s

pybabel update -i locale/base.pot -d locale

# Compile Strings

pybabel compile -d locale

# Extract Strings (Nicht benutzen!):

pybabel extract . -o locale/base.pot
pybabel init -l en_GB de_DE -i locale/base.pot -d locale
pybabel init -l de_DE -i locale/base.pot -d locale

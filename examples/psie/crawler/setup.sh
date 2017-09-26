. ~/.bash_profile
pyenv local 3.6.1
mkdir zip
python gadm.py
python parse.py > data.list
mv data.list ../web/

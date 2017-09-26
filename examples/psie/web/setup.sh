git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT=$HOME/.pyenv' >> ~/.bash_profile
echo 'export PATH=$PYENV_ROOT/bin:$PATH' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile

. ~/.bash_profile

pyenv install 3.6.1
pyenv local 3.6.1

pip install -r requirements.txt

PGPASSWORD=psie psql -f dump.sql -U psie

python make2.py

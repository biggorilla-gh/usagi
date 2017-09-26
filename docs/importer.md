# Import databases into Usagi for search

## A. Write a configuration file:
to teach Usagi to access the databases which you want to manage. (In the future, Usagi plans to also take metadata directly to avoid accessing user databases if needed for security reasons.) For example,

~~~ini
[ClassicModels]
data_store: psql
host: localhost
port: 5432
user: classic_user
dbname: classicmodels
password: password
~~~

## B. Execute the Usagi installer:

~~~bash
./usagi-installer --data-store classic_models.cfg
~~~

## C. Start Solr server and JSON API

~~~bash
./solr/solr/bin/solr start
cd api
pkill -KILL api_server.py
python api_server.py &
cd ..
~~~

## D. Search

~~~bash
cd importer
python search.py <your_favourite_keyword>
~~~

## E. JSON API

~~~bash
curl http://localhost:8085/api/search?q=<your_favourite_keyword>
~~~

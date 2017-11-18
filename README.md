Usagi
===

Usagi is a data discovery system for Recruit’s internal infrastructure. Usagi crawls metadata within Recruit's web services every day and builds a catalog of data sets. Usagi enables users to search, monitor, and annotate the metadata which helps them discover the appropriate data to perform analysis.

Many large enterprises today witness an explosion in the number of data sets.  Therefore, we aim to make Usagi open source. We hope Usagi helps data-users in these enterprises discover meaningful data easily.  The members who invent Usagi are contributors of Meta-Looking in Recruit Holdings Co., Ltd. and GOODS [1].

[1] Halevy, Alon, et al. "Goods: Organizing Google's Datasets." Proceedings of the 2016 International Conference on Management of Data. ACM, 2016.


# Setup Usagi
* A. Write a configuration file to teach Usagi to access the databases which you want to manage. (In the future, Usagi plans to also take metadata directly to avoid accessing user databases if needed for security reasons.) For example,

```ini
[ClassicModels]
data_store: psql
host: localhost
port: 5432
user: classic_user
dbname: classicmodels
password: password
```

* B. Execute the Usagi installer:

```bash
./usagi-installer --data-store classic_models.cfg
```

* C. Start Solr server and JSON API

```bash
./solr/solr/bin/solr start
cd api
pkill -KILL api_server.py
python api_server.py &
cd ..
```

* D. Try to search

```bash
cd importer
python search.py <your_favourite_keyword>
```

* E. Try JSON API

```bash
curl http://localhost:8085/api/search?q=<your_favourite_keyword>
```

# Run test

```bash
./test/run_test.sh

# create and run a docker container....

pytest # in the docker container
```

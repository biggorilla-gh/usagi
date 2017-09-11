node {
  checkout scm
  stage("docker build") {
    docker.build("usagi")
  }

  stage("boot docker") {
    docker.image("usagi").inside("-u 0:0") {

      stage("Boot services") {
        sh '/etc/init.d/mariadb restart'
        sh '/etc/init.d/postgresql restart'
      }

      stage("checkout") {
        checkout scm
      }

      stage("Create database") {
        sh "psql -U postgres -f sql/create_database.sql"
        sh "PGPASSWORD=usagi psql -U usagi -f sql/create_table.sql usagi"
      }

      stage("Import test data (postgresql)") {
        sh "psql -U postgres -f test/data/create_classic_user_and_db.psql"
        sh "PGPASSWORD=password psql -U classic_user -f test/data/ClassicModels.psql classicmodels"
      }

      stage("Import test data (mysql)") {
        sh "mysql -u root -proot < test/data/create_mysql_db.sql"
        sh "unzip test/data/sportsdb.zip -o -d test/data"
        sh "mysql -u root -proot sportsdb < test/data/sportsdb.sql"
        sh "unzip test/data/sakila.zip -o -d test/data"
        sh "mysql -u root -proot sakila < test/data/sakila.sql"
        sh "unzip test/data/employees.zip -o -d test/data"
        sh "mysql -u root -proot employees < test/data/employees.sql"
      }

      stage("pip install") {
        sh 'pip install -r requirements.txt'
      }

      stage("Setup usagi") {
        sh 'bash usagi-installer --data-store ./test/psql_mysql/search.ini'
        sh 'sleep 5'
        sh 'solr/solr/bin/solr start -force'
        sh 'sleep 5'
      }

      stage('Test') {
        sh 'py.test test/'
      }
    }
  }  
}


DEST=solr-6.3.0
CORE=psie
CORE_PATH=$DEST/server/solr/$CORE

curl http://archive.apache.org/dist/lucene/solr/6.3.0/solr-6.3.0.tgz -o solr.tgz
mkdir $DEST
tar zxvf solr.tgz -C $DEST --strip=1

$DEST/bin/solr start
sleep 5
$DEST/bin/solr create -c $CORE

mkdir -p $CORE_PATH/conf
cp -R solr_config/conf/* $CORE_PATH/conf/
mkdir -p $CORE_PATH/lib
cp -R solr_config/lib/* $CORE_PATH/lib/
cp -R solr_config/WEB-INF/lib/* $DEST/server/solr-webapp/webapp/WEB-INF/lib/
$DEST/bin/solr restart

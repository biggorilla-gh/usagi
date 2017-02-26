DEST=solr
PORT=8982
CORE=usagi
CORE_PATH=$DEST/server/solr/$CORE
JAR=solr-1.0.2.jar

./gradlew jar
cp build/libs/$JAR solr_config/lib/$JAR

rm -rf $DEST

curl http://archive.apache.org/dist/lucene/solr/6.3.0/solr-6.3.0.tgz -o solr.tgz
mkdir $DEST
tar zxvf solr.tgz -C $DEST --strip=1

echo "SOLR_PORT=$PORT" >> $DEST/bin/solr.in.sh

$DEST/bin/solr start
sleep 10
$DEST/bin/solr create -c $CORE

cp -R solr_config/WEB-INF/lib/* $DEST/server/solr-webapp/webapp/WEB-INF/lib/

cp -R solr_config/conf/* $CORE_PATH/conf/
rm -rf $CORE_PATH/lib/*
mkdir $CORE_PATH/lib
cp -R solr_config/lib/* $CORE_PATH/lib/

$DEST/bin/solr restart


DEST=solr
PORT=8982
CORE=usagi
CORE_PATH=$DEST/server/solr/$CORE
JAR=solr-1.0.2.jar

rm -rf $DEST

curl http://archive.apache.org/dist/lucene/solr/6.3.0/solr-6.3.0.tgz -o solr.tgz
mkdir $DEST
tar zxvf solr.tgz -C $DEST --strip=1
rm solr.tgz

echo "SOLR_PORT=$PORT" >> $DEST/bin/solr.in.sh

$DEST/bin/solr start
sleep 10
$DEST/bin/solr create -c $CORE

#cp -R solr_config/WEB-INF/lib/* $DEST/server/solr-webapp/webapp/WEB-INF/lib/
wget -O jts.zip https://sourceforge.net/projects/jts-topo-suite/files/jts/1.14/jts-1.14.zip/download
unzip jts.zip lib/jts-1.14.jar
unzip jts.zip lib/jtsio-1.14.jar
rm jts.zip
curl http://central.maven.org/maven2/com/vividsolutions/jts-core/1.14.0/jts-core-1.14.0.jar -o jts-core-1.14.0.jar
curl http://central.maven.org/maven2/org/noggit/noggit/0.7/noggit-0.7.jar -o noggit-0.7.jar
mv lib/jts-1.14.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/ 
mv lib/jtsio-1.14.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/
mv jts-core-1.14.0.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/
mv noggit-0.7.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/
rmdir lib

cp -R conf/* $CORE_PATH/conf/
rm -rf $CORE_PATH/lib/*
mkdir $CORE_PATH/lib

#cp -R solr_config/lib/* $CORE_PATH/lib/
curl http://central.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/1.0.5-3/kotlin-stdlib-1.0.5-3.jar -o kotlin-stdlib-1.0.5-3.jar
mv kotlin-stdlib-1.0.5-3.jar $CORE_PATH/lib/

./gradlew jar
cp build/libs/$JAR $CORE_PATH/lib/

$DEST/bin/solr restart


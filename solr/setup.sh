DEST=solr
PORT=8982
CORE=usagi
CORE_PATH=$DEST/server/solr/$CORE
JAR=solr-1.0.2.jar
DOWNLOAD_DIR=downloads

function download {
	sha1=$1
	filepath=$DOWNLOAD_DIR/$2
	url=$3

  download=0
	if [ -f $filepath ]; then
		local_sha1=`openssl sha1 $filepath | cut -d ' ' -f 2`
		if [ $sha1 != $local_sha1 ]; then
			download=1
		fi
	else
		download=1
	fi

	if [ $download = 1 ]; then
		curl $url -L -o $filepath
	fi

}

if [ -f $DEST/bin/solr ]; then
  $DEST/bin/solr stop -force
fi

rm -rf $DEST
mkdir $DOWNLOAD_DIR

download 8e11c1d7af0ac516f6a2e7e1a486d216cc9944b8 solr.tgz http://archive.apache.org/dist/lucene/solr/6.3.0/solr-6.3.0.tgz

mkdir $DEST
tar zxvf $DOWNLOAD_DIR/solr.tgz -C $DEST --strip=1

echo "SOLR_PORT=$PORT" >> $DEST/bin/solr.in.sh

$DEST/bin/solr start -force
sleep 5
$DEST/bin/solr create -c $CORE -p $PORT -force

download 2b78bbd7df747b74498766a1cc12af822a6a1a33 jts.zip https://sourceforge.net/projects/jts-topo-suite/files/jts/1.14/jts-1.14.zip/download

rm -f lib/jts-1.14.jar
rm -f lib/jtsio-1.14.jar
unzip $DOWNLOAD_DIR/jts.zip lib/jts-1.14.jar
unzip $DOWNLOAD_DIR/jts.zip lib/jtsio-1.14.jar

download ff63492fba33a395f0da17720dd1716aba0d8c84 jts-core-1.14.0.jar http://central.maven.org/maven2/com/vividsolutions/jts-core/1.14.0/jts-core-1.14.0.jar

download 33ff21a52ac715fb760519cb3cfd150178ebe207 noggit-0.7.jar http://central.maven.org/maven2/org/noggit/noggit/0.7/noggit-0.7.jar

cp lib/jts-1.14.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/
cp lib/jtsio-1.14.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/
cp $DOWNLOAD_DIR/jts-core-1.14.0.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/
cp $DOWNLOAD_DIR/noggit-0.7.jar $DEST/server/solr-webapp/webapp/WEB-INF/lib/
rm -rf lib

cp -R conf/* $CORE_PATH/conf/
rm -rf $CORE_PATH/lib/*
mkdir $CORE_PATH/lib

download 306c2e49fcf7f0f66470565db443bab97612fdea kotlin-stdlib-1.0.5-3.jar http://central.maven.org/maven2/org/jetbrains/kotlin/kotlin-stdlib/1.0.5-3/kotlin-stdlib-1.0.5-3.jar

cp $DOWNLOAD_DIR/kotlin-stdlib-1.0.5-3.jar $CORE_PATH/lib/

./gradlew jar
cp build/libs/$JAR $CORE_PATH/lib/

$DEST/bin/solr stop -force
sleep 5
$DEST/bin/solr start -force
sleep 5


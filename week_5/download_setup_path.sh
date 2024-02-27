#!/bin/bash

TOOL_FOLDER="D:\\APP/tools"

#set JAVA_HOME, after you download jdk, you can find it in your TOOL_FOLDER and extract it
cd $TOOL_FOLDER
JAVA_FOLDER="jdk-11.0.21"
export JAVA_HOME="${TOOL_FOLDER}/${JAVA_FOLDER}" 
# export PATH="${JAVA_HOME}/bin:${PATH}"


#download hadoop
cd $TOOL_FOLDER

HADOOP_VERSION="3.2.0"
HADOOP_FOLDER="hadoop-${HADOOP_VERSION}"
HADOOP_BIN_FOLDER="${HADOOP_FOLDER}/bin"
HADOOP_PREFIX="https://raw.githubusercontent.com/cdarlint/winutils/master/hadoop-${HADOOP_VERSION}/bin/"
HADOOP_FILES="hadoop.dll hadoop.exp hadoop.lib hadoop.pdb libwinutils.lib winutils.exe winutils.pdb"

mkdir $HADOOP_FOLDER
mkdir $HADOOP_BIN_FOLDER

for FILE in ${HADOOP_FILES}; do
  file_path="${HADOOP_BIN_FOLDER}/${FILE}"

  if ! [ -f "$file_path" ]; then
    echo "Downloading ${FILE}"
    curl -L "${HADOOP_PREFIX}/${FILE}" -o "$file_path"
  fi
done

export HADOOP_HOME="${TOOL_FOLDER}/${HADOOP_FOLDER}"
# export PATH="${HADOOP_HOME}/bin:${PATH}"


#download spark

cd $TOOL_FOLDER
SPARK_FOLDER="spark-3.3.2-bin-hadoop3"
SPARK_URL="https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz"

if ! [ -f "${SPARK_FOLDER}.tgz" ]; then
    echo "Downloading Spark"
    curl -L $SPARK_URL -o spark-3.3.2-bin-hadoop3.tgz
fi

tar -xzf spark-3.3.2-bin-hadoop3.tgz

export SPARK_HOME="${TOOL_FOLDER}/${SPARK_FOLDER}"
# export PATH="${SPARK_HOME}/bin:${PATH}"

echo $JAVA_HOME
echo $HADOOP_HOME
echo $SPARK_HOME

cd $SPARK_FOLDER

./bin/spark-shell.cmd


# export JAVA_HOME="D:\APP/tools/jdk-11.0.21"
# export HADOOP_HOME="D:\APP/tools/hadoop-3.2.0"
# export SPARK_HOME="D:\APP/tools/spark-3.3.2-bin-hadoop3"
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$SPARK_HOME/bin:$PATH
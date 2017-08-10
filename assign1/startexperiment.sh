#!/bin/bash

PWD=`pwd`

horizon=100000
port=5001
nRuns=100
hostname="localhost"
banditFile="$PWD/data/instance-5.txt"

algorithm="Thompson-Sampling"
# Allowed values for algorithm parameter(case-sensitive)
# 1. epsilon-greedy 
# 2. UCB 
# 3. KL-UCB 
# 4. Thompson-Sampling
# 5. rr

epsilon=0.1

numArms=$(wc -l $banditFile | cut -d" " -f1 | xargs)

SERVERDIR=./server
CLIENTDIR=./client

OUTPUTFILE=$PWD/serverlog.txt
OUTPUTFILE2=$PWD/clientlog.txt
ERRORFILE=$PWD/clienterror.txt

randomSeed=0

pushd $SERVERDIR
cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE &"
#echo $cmd
$cmd 
popd

sleep 1

pushd $CLIENTDIR
cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon $OUTPUTFILE2 $ERRORFILE &"
#echo $cmd
$cmd > /dev/null 
popd


#!/bin/bash


echo $#
if [ $($#) > 2 ]
then
    printf "Número de argumentos inválido.\nUtilização: bash build.sh <nome_container>"
    exit 1
fi

container=${BASH_ARGV[0]}

sudo docker build -t $container -f recon/$container/Dockerfile .

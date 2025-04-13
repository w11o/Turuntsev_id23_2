#!/bin/bash

sudo apt update

sudo apt install -y build-essential git

git clone https://github.com/openwall/john

cd john

./configure && make -s clean && make -sj4

sudo cp run/*.john /usr/local/bin/
sudo cp run/rar2john /usr/local/bin/

sudo chmod +x /usr/local/bin/rar2john

rar2john --help

echo "Установка завершена."

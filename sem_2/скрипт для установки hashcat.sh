#!/bin/bash

sudo apt update

sudo apt install hashcat

if [ -x "$(command -v hashcat)" ]; then
    echo "Hashcat успешно установлен."
else
    echo "Ошибка установки hashcat."
fi

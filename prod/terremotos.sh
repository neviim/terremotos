#! /bin/bash
# virtualenv agora esta ativ0
# /home/jorge/src/terremotos/src/src
#
# A cada 30 minutos sera executado, coloque a linha abaixo no crontab.
#
# nano /etc/crontab
#   0,30 * * * * /home/jorge/src/terremotos/prod/terremotos.sh
#
source /home/jorge/virtual/py37/bin/activate
cd /home/jorge/src/terremotos/prod/
python terremotos.py
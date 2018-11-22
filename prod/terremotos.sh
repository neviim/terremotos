#!/bin/zsh

# virtualenv agora esta ativ0
# /home/neviim/src/_projetos/terremotos/src
#
# A cada 30 minutos sera executado, coloque a linha abaixo no crontab.
#
# nano /etc/crontab
#   0,30 * * * * sh /home/neviim/src/_projetos/terremotos/prod/terremotos.sh
#
# chsh -l

source /home/neviim/virtual/py37/bin/activate
cd /home/neviim/src/_projetos/terremotos/prod
python terremotos.py > /tmp/arangomot.log
date >> /tmp/arangomot.log

#deactivate
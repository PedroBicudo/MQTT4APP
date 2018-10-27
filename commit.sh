#!/bin/bash 

#--------------------------------------------
#
#
# AUTOR: PH
# DATA: 27/10/2018
#
#
# VERSION: 1
# NAME: commit.sh
#
# 
#
# OBJETIVO: COMMIT NO GITHUB
#
#
#--------------------------------------------

# Root
[ "$UID" = "0" ] && echo "Root não permitido" && exit 1

# Arquivo
[ -z "$1" ] && echo "Arquivo não apontado" && exit 1

# commit info 
data=$( date +%D)

# Enviando informação
git status 
git add $1 
git commit -m  $data
git push -u origin master
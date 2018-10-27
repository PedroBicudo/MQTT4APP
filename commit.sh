#!/bin/bash

# ---------------------------------------------
#
#
# AUTOR: SRKFY
# DATA: 10/27/2018
#
# VERSION: 1
# NOME: commit.sh
#
# OBJETIVO: Commit Github
#
# ---------------------------------------------

#data commit
data=$( date +%D)
# Root 
[ "$UID" = "0" ] && echo "Root não permitido." && exit 1

# File Verification
[ -z "$1" ] && echo "Arquivo não especificado." && exit 1

git add $1
git commit -m "$data"
git push -u origin master
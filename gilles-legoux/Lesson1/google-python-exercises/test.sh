#!/usr/bin/env bash

PYTHON="python"

SUCCESS_TOT=0
FAILURE_TOT=0

BLUE='\033[1;34m'
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd "$(dirname "$0")"

function print_result() {
  local success="$1"
  local failure="$2"
  if test ${failure} -eq 0; then
    echo -en ">>>> ${GREEN}OK: "
  else
    echo -en ">>>> ${RED}KO: "
  fi
  echo -n "TEST ${success}/$((${success} + ${failure})), "
  echo -n "${success} success, ${failure} failure."
  echo -e "${NC}\n"
}

function test_folder() {
  local folder="$1"
  local exs="$2"
  local output
  local success
  local failure
  echo -e "${BLUE}*** ${folder} ***${NC}\n"
  cd "${folder}"
  OLDIFS=$IFS
  IFS=$','
  for ex in ${exs}; do
    echo -ne "${YELLOW}--> ${folder}/${ex}${NC}\n"
    IFS=$OLDIFS
    output=`${PYTHON} ${ex}`
    IFS=$','
    echo "$output" | grep -E --color "^  X.*|^"
    success=`echo "${output}" | grep -E "^ OK" | wc -l`
    failure=`echo "${output}" | grep -E "^  X" | wc -l`
    SUCCESS_TOT=$((${SUCCESS_TOT} + ${success}))
    FAILURE_TOT=$((${FAILURE_TOT} + ${failure}))
    if test $((${success} + ${failure})) -eq 0; then
      echo -e ">>>> No Test.\n"
    else
      print_result ${success} ${failure}
    fi
  done
  IFS=$OLDIFS
  cd - > /dev/null
}

echo -e "\nTests of Google Python exercises"
echo -e "================================\n"

test_folder "basic" "list1.py,list2.py,string1.py,string2.py,"\
"wordcount.py --count small.txt,"\
"wordcount.py --topcount small.txt,"\
"wordcount.py --topcount alice.txt,"\
"mimic.py small.txt,"\
"mimic.py alice.txt"\

echo -e "\nResults"
echo -e "=======\n"
print_result ${SUCCESS_TOT} ${FAILURE_TOT}

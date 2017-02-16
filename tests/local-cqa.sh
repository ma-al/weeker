#!/bin/bash
# Run code quality assurance (CQA) checks locally.

function section
{
   echo;echo;
   echo "================================================================ [$1]"
   echo
}

MODULE="weeker"

section "pytest"
coverage run --source $MODULE -m py.test -vs
echo "Completed. Exit code: $?"

section "coverage"
coverage report --fail-under=70 -m
echo "Completed. Exit code: $?"

# Remove `-rn` if you want to see full output
section "pylint"
pylint $MODULE -rn
echo "Completed. Exit code: $?"

section "flake8"
flake8 $MODULE --count
echo "Completed. Exit code: $?"

echo

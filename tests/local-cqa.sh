#!/bin/bash
# Run code quality assurance (CQA) checks locally.

function section
{
   echo;echo;
   echo "================================================================ [$1]"
   echo
}

MODULE="weeker"

# Coming soon...
#section "coverage"
#coverage run --source $MODULE -m py.test
#coverage report -m

# Remove `-rn` if you want to see full output
section "pylint"
pylint $MODULE -rn
echo;echo "Completed. Exit code: $?"

section "flake8"
flake8 $MODULE --count
echo;echo "Completed. Exit code: $?"

echo

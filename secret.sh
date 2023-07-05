#!/bin/bash
declare -a ARR=$ALL_SECRET

for SECRET_NAME in "${ARR[@]}"
do
    vlt secrets get --plaintext $SECRET_NAME | tr -d '\n' > input.txt;
    output="$(base64 -w 0 < input.txt)";
    echo "Patching secret $SECRET_NAME";
    kubectl patch secret $SECRETS_NAME -p="{\"data\":{\"$SECRET_NAME\": \"$output\"}}" -n $namespace -v=1;
done
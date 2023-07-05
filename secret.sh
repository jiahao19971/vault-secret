#!/bin/bash
declare -a ARR=$ALL_SECRET

for SECRET_NAME in "${ARR[@]}"
do
    output="$(vlt secrets get --plaintext $SECRET_NAME | base64)";
    echo $output;
    kubectl patch secret $SECRETS_NAME -p="{\"data\":{\"$SECRET_NAME\": \"$output\"}}" -n $namespace -v=1;
done
#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: ./fetcher.sh -d example.com -w wordlist.txt [-o output.txt]"
    exit 1
fi

while getopts "d:w:o:" opt; do
    case ${opt} in
        d ) domain=$OPTARG ;;
        w ) wordlist=$OPTARG ;;
        o ) output=$OPTARG ;;
        * ) echo "Invalid option"; exit 1 ;;
    esac
done

if [ -z "$domain" ] || [ -z "$wordlist" ]; then
    echo "Error: Domain and wordlist are required!"
    exit 1
fi

echo "Starting DNS brute-force for $domain..."

while IFS= read -r subdomain; do
    full_subdomain="$subdomain.$domain"
    ip=$(dig +short "$full_subdomain" | head -n 1)
    if [ -n "$ip" ]; then
        echo "[+] Found: $full_subdomain -> $ip"
        if [ -n "$output" ]; then
            echo "$full_subdomain ($ip)" >> "$output"
        fi
    fi
done < "$wordlist"

echo "Brute-force completed."

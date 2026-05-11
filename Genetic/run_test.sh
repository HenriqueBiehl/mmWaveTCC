#!/bin/bash

runs=30
total_time=0
total_fitness=0

if [ -z "$1" ]; then
    echo "Uso: $0 <arquivo_entrada>"
    exit 1
fi

input_file=$1

for i in $(seq 1 $runs); do
    #output=$(python3 main.py -c -g 4500 -t 5 -mc 2 < "$input_file")
    output=$(python3 main.py < "$input_file")

    # Pega só a última linha relevante
    line=$(echo "$output" | grep "Max fitness")

    # Extrai fitness
    fitness=$(echo "$line" | grep -oP '=\s*\K[0-9.]+')

    # Extrai tempo
    time=$(echo "$line" | grep -oP 'found in \K[0-9.]+')

    total_time=$(echo "$total_time + $time" | bc)
    total_fitness=$(echo "$total_fitness + $fitness" | bc)

    printf "Run %02d -> fitness=%s | time=%s\n" "$i" "$fitness" "$time"
done

avg_time=$(echo "scale=4; $total_time / $runs" | bc)
avg_fitness=$(echo "scale=4; $total_fitness / $runs" | bc)

echo "----------------------"
echo "Média do tempo: $avg_time secs"
echo "Média do fitness: $avg_fitness Gbps"
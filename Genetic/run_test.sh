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
    output=$(python3 main.py -c -g 5 -t 700 -mc 5 < "$input_file")

    # Pega só a última linha relevante
    line=$(echo "$output" | grep "Max fitness")

    # Extrai fitness
    fitness=$(echo "$line" | grep -oP '=\s*\K[0-9.]+')

    # Extrai tempo
    time=$(echo "$line" | grep -oP 'found in \K[0-9.]+')

    total_time=$(echo "$total_time + $time" | bc)
    total_fitness=$(echo "$total_fitness + $fitness" | bc)

    echo "Run $i -> fitness=$fitness | time=$time"
done

avg_time=$(echo "scale=4; $total_time / $runs" | bc)
avg_fitness=$(echo "scale=4; $total_fitness / $runs" | bc)

echo "----------------------"
echo "Média do tempo: $avg_time secs"
echo "Média do fitness: $avg_fitness Gbps"
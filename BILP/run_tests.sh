#!/bin/bash

if [ -z "$1" ]; then
    echo "Uso: $0 <arquivo_entrada>"
    exit 1
fi

input_dir=$1
runs=30

total_time=0
total_objective_sum=0

for i in $(seq 1 $runs); do
    output=$(python3 BILP.py -d "$input_dir")

    # Soma todos os objectives dessa execução
    obj_sum=$(echo "$output" | grep "Objective =" | awk '{sum += $3} END {print sum}')

    # Pega o tempo
    time=$(echo "$output" | grep "Results found in" | grep -oP '[0-9.]+(?= secs)')

    total_time=$(echo "$total_time + $time" | bc)

    echo "Run $i -> obj_sum=$obj_sum | time=$time"
done

avg_time=$(echo "scale=6; $total_time / $runs" | bc)

echo "----------------------"
echo "Média do tempo: $avg_time secs"
echo "Objetivo total: $obj_sum Gbps"
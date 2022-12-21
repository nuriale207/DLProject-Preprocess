#!/bin/bash

# Directorio de origen
src_dir=$1

# Directorios de destino
train_dir=$1/train
test_dir=$1/test
dev_dir=$1/dev

# Crea los directorios de destino si no existen
mkdir -p $train_dir $test_dir $dev_dir

# Obtiene la lista de archivos en el directorio de origen
files=$(find $src_dir -type f)

# Calcula el número total de archivos
total_files=$(echo "$files" | wc -l)

total_files=$(echo "scale=1; $total_files / 1" | bc)


# Calcula el número de archivos a mover a cada directorio
train_files=$(awk -v x=0.7 -v y=$total_files 'BEGIN{printf "%.2f", x*y}')
train_files=$(awk -v x=$train_files 'BEGIN{printf "%.0f", x}')

test_files=$(awk -v x=0.15 -v y=$total_files 'BEGIN{printf "%.2f", x*y}')
test_files=$(awk -v x=$test_files 'BEGIN{printf "%.0f", x}')

dev_files=$(awk -v x=0.15 -v y=$total_files 'BEGIN{printf "%.2f", x*y}')
dev_files=$(awk -v x=$dev_files 'BEGIN{printf "%.0f", x}')


# Mueve los archivos al directorio de entrenamiento
count=0
while [ $count -lt $train_files ]; do
  file=$(echo "$files" | head -n 1)
  cp "$file" "$train_dir"
  files=$(echo "$files" | tail -n +2)
  count=$((count + 1))
done

# Mueve los archivos al directorio de prueba
count=0
while [ $count -lt $test_files ]; do
  file=$(echo "$files" | head -n 1)
  cp "$file" "$test_dir"
  files=$(echo "$files" | tail -n +2)
  count=$((count + 1))
done

# Mueve los archivos al directorio de desarrollo
count=0
while [ $count -lt $dev_files ]; do
  file=$(echo "$files" | head -n 1)
  cp "$file" "$dev_dir"
  files=$(echo "$files" | tail -n +2)
  count=$((count + 1))
done
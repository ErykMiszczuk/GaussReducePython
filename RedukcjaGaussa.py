import sys
import io
import os
import re
import csv

input_path = './dane/'
output_path = './output/'

def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

list_of_files = []
for (dirpath, dirnames, filenames) in os.walk(input_path):
    list_of_files.extend(filenames)
    break

matrix = []
print(list_of_files)
new_matrix = []
for file_name in list_of_files:
    input_args = re.search(r"(\d+)_(\d+)_(\d+)", file_name)
    # print(input_args.group())
    liczba_kolumn = int(input_args.group(2))
    liczba_wierszy = int(input_args.group(3))
    print('Liczba wierszy macierzy: {}, liczba kolumn: {}'.format(liczba_wierszy, liczba_kolumn))
    with open(input_path + file_name, 'r') as data:
        reader = csv.reader(data)
        matrix = list(reader)
        tmpColumn = []
        for n in range(0, liczba_kolumn):
            for m in range(1, liczba_wierszy+1):
                tmpColumn.append(matrix[n][2*m-2:2*m])
            
            # print(tmpColumn)
            new_matrix.append(tmpColumn)
            tmpColumn = []
        
        print(matrix)
        print(new_matrix)
        new_matrix = []
    
    with open(output_path + file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',', quotechar = '\'', quoting = csv.QUOTE_MINIMAL)
        writer.writerows(new_matrix)
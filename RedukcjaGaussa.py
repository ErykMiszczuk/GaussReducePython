import sys
import io
import os
import re
import csv

INFINITY = float("inf")

input_path = './dane/'
output_path = './Wynik426197/'
from_last_recursion_pos = [[0,0]]

def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

list_of_files = []
for (dirpath, dirnames, filenames) in os.walk(input_path):
    list_of_files.extend(filenames)
    break

def check_columns(matrix, cols, rows):
    for i in range(0,rows):
        if (int(matrix[i][cols][0]) / int(matrix[i][cols][1])) == 0:
            return True
        else:
            return False 

def check_column_for_zero(matrix, col, rows):
    index = -1
    for i in range(0,rows):
        if (int(matrix[i][col][0]) / matrix[i][col][1]) == 0:
            continue
        else:
            index = i
    
    return index 

def min_in_matrix_col(inmatrix, col, rows):
    minimum = INFINITY
    index = -1
    for i in range(0, rows):
        if (int(matrix[i][col][0]) / int(matrix[i][col][1])) < minimum:
            minimum = int(matrix[i][col][0]) / int(matrix[i][col][1])
          
    return index

def ret_col_from_matrix(inmatrix, rows):
    tmpColumn = []
    for row in range(0, rows):
        tmpColumn.append(inmatrix[row][0])

    return tmpColumn

def operations_factory(list, reduce_row, reduce_col):
    cur_row, cur_col = list[-1]
    pos = [cur_row + reduce_row, cur_col + reduce_col]
    list.append(pos)

def Gauss(inmatrix, cols, rows):
    if check_columns(inmatrix, 0, rows) == True:
        #Go to 2
        if liczba_kolumn == 1:
            return inmatrix
        else:
            operations_factory(from_last_recursion_pos, 0, 1)
            return Gauss(inmatrix[0:rows][1:cols], cols - 1, rows)
    else:
        #Go to 3
        if int(inmatrix[0][0][0]) / int(inmatrix[0][0][1]) == 0:
          #Go to 4
            min_index = check_column_for_zero(inmatrix, 0, rows)
            # Swap the rows
            inmatrix[0], inmatrix[min_index] = inmatrix[min_index], inmatrix[0]
            list_of_elementar_operations.append('Zamiana wiersza {} na wiersz {}'.format(from_last_recursion_pos[-1][0], min_index + from_last_recursion_pos[-1][0]))
        #Go to 5
        for j in range(2, rows):
            for col in range(0, cols):
                print(inmatrix[j][col])
                tmp_val_a = int(inmatrix[j][col][0]) * int(inmatrix[j][0][1])
                tmp_val_b = int(inmatrix[j][col][1]) * int(inmatrix[j][0][0])
                tmp_val = [tmp_val_a, tmp_val_b]
                multiplier = (tmp_val_a/tmp_val_b)
                multiplier *= int(inmatrix[j][col][0])
                if inmatrix[j][col][1] == tmp_val[1]:
                    inmatrix[j][col][0] = int(inmatrix[j][col][0]) - (multiplier * tmp_val[0])
                else:
                    #Wyrównanie mianowników poprzez wymnożenie ich przez siebie i opowiednie przemnożenie liczników
                    a = int(inmatrix[j][col][1])
                    b = int(inmatrix[j][col][0])
                    inmatrix[j][col][0] = b * tmp_val[1]
                    inmatrix[j][col][1] = a * tmp_val[1]
                    tmp_val[1] *= a
                    tmp_val[1] *= b
                    inmatrix[j][col][0] = int(inmatrix[j][col][0]) - (multiplier * tmp_val[0])
                    list_of_elementar_operations.append('Odjęcie od wiersza {} wiersza {} przemnożonego przez {} '.format(from_last_recursion_pos[-1][0], (min_index + from_last_recursion_pos[-1][0]), multiplier))
        if m != 1:
            #Return gauss
            operations_factory(from_last_recursion_pos, 0, 1)
            return Gauss(inmatrix[1:rows][1:cols], cols - 1, rows - 1)
        else:
            #Return vector
            return ret_col_from_matrix(inmatrix, rows)


matrix = []
list_of_elementar_operations = []
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
        # Operations on new_matrix
        Gauss(new_matrix, liczba_kolumn, liczba_wierszy)
        print('\n')
        print(list_of_elementar_operations)
        # End operations on the matrix

    with open(output_path + file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',', quotechar = '\'', quoting = csv.QUOTE_MINIMAL)
        writer.writerows(new_matrix)
    
    new_matrix = []
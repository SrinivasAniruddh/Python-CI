import argparse
import os.path
import csv
import matplotlib.pyplot as graph
from numpy import *

""" Variables """
file_dictionary = {}
sorted_list = []

def parser_function():
    """ Take arguments from command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", type=str, help="Enter the .date file with the path")
    parser.add_argument("delimiter", type=str, help="Delimiter used in the file")
    arguments = parser.parse_args()
    input_file = [arguments.data_file, arguments.delimiter]
    print("The files are", input_file)
    return input_file

def parse_file(data_file, delimiter):
    """ This function validates the file existence and parses it """
    assert os.path.isfile(data_file), "Please enter the correct file name with the abs path"
    with open(data_file, "r") as file_handler:
        csv_reader = csv.reader(file_handler, delimiter=delimiter)
        refined_list = []
        for line in csv_reader:
            print("The line is {}".format(line))
            newline = []
            for value in line:
                if set_data_type(value) is not None:
                    newline += [set_data_type(value)]
                    print("The list is {}".format(newline))
            if len(newline) > 0:
                refined_list.append(newline)
    print("Refined list is {}".format(refined_list))
    return refined_list

def determine_header_presence(list_of_values):
    """ This function determines the presence of a header by validating the data type of the first coloumn with that of the subsequent columns """
    for idx, col in enumerate(list_of_values[0]):
        print("Col is ",col)
        for row in list_of_values:
            print("The row is ",row)
            print(row[idx])
            if (type(row[idx]) is not type(col)):
                try:
                    if ((int(row[idx]) or float(row[idx])) and (int(col) or float(col))):
                        print("Index is ",row[idx])
                except:
                    return True
        return False

def set_data_type(value):
    """ This function sets the data type of the given value """
    if value == "":  # len(element) == 0
        return None
    try:
        intended_value = int(value)
    except ValueError:
        try:
            intended_value = float(value)
        except ValueError:
            intended_value = str(value)
    finally:
        return intended_value

def set_headers(consol_list, first_row_header):
    """ Sets headers for a given list of lists """
    if first_row_header is True:
        sorted_list = consol_list[1:]
        file_dictionary = create_dictionary(consol_list[0], sorted_list)
    else:
        headers = list(range(1, len(consol_list[0]) + 1))
        file_dictionary = create_dictionary(headers, consol_list)
    return file_dictionary

def create_dictionary(headers, sorted_list):
    for column_id, header in enumerate(headers):
        file_dictionary[header] = []
        for rows in sorted_list:
            file_dictionary[header] += [rows[column_id]]
    return file_dictionary

def plot_graphs(file_dictionary):
    size = len(file_dictionary.keys())
    graph.subplots(size, size, figsize=(80,80))
    graph.rcParams.update({'font.size': 8})
    for column_1_index, column_1 in enumerate(file_dictionary.keys()):
        for column_2_index, column_2 in enumerate(file_dictionary.keys()):
            graph.xlabel(column_1)
            graph.ylabel(column_2)
            x=array(file_dictionary[column_1])
            y=array(file_dictionary[column_2])
            linear = polyfit(x, y, 1)
            degree_2 = polyfit(x, y, 2)
            degree_3 = polyfit(x, y, 3)
            degree_4 = polyfit(x, y, 4)
            xp = linspace(min(x), max(x), len(x) // 2)
            graph.subplot2grid(shape=(size,size), loc=(column_1_index, column_2_index))
            graph.plot(x, y, '.')
            graph.plot(xp, polyval(linear, xp), 'g--', label='linear')
            graph.plot(xp, polyval(degree_2, xp), 'c--', label='square')
            graph.plot(xp,polyval(degree_3,xp), 'y--', label='cubic')
            graph.plot(xp, polyval(degree_4, xp), 'm--', label='quadra')
            graph.title("{0} x {1}".format(column_1, column_2))
            graph.legend(loc='upper right')
    graph.savefig("Myfinal-1.png", bbox_inches='tight')

def main():
    input_file = parser_function()
    print("The file is {}".format(input_file[0]))
    refined_list_of_values = parse_file(input_file[0], input_file[1])
    header = determine_header_presence(refined_list_of_values)
    file_dictionary = set_headers(refined_list_of_values, header)
    print("The dictionary is {}".format(file_dictionary))
    plot_graphs(file_dictionary)

if __name__ == "__main__":
    main()
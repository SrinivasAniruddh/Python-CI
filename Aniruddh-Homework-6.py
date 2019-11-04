import argparse
import os.path
import csv
import matplotlib.pyplot as graph
import numpy as np
import scipy.interpolate as sci_ip

""" Variables """
file_dictionary = {}
sorted_list = []


def parser_function():
    """ Take arguments from command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", type=str, help="Enter the .date file with the path")
    parser.add_argument("delimiter", type=str, help="Delimiter used in the file")
    parser.add_argument("--plot", "-p", type=str, help="Enter Yes if you would like to plot graphs")
    parser.add_argument("--summary", "-s", type=str, help="Enter the column name to calculate mean, standard "
                                                          "deviation and indentify if the data is "
                                                          "categorical/descrete")
    parser.add_argument("--interpolate", "-ip", nargs='+', help="Enter two column names and the value in the first "
                                                                "column")
    arguments = parser.parse_args()
    if len(arguments.interpolate) != 3:
        raise Exception("Enter exactly 3 values for interpolate argument")
    input_file = [arguments.data_file, arguments.delimiter, arguments.plot, arguments.summary, arguments.interpolate]
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
    """ This function determines the presence of a header by validating the data type of the first column with that
    of the subsequent columns """
    for idx, col in enumerate(list_of_values[0]):
        print("Col is ", col)
        for row in list_of_values:
            print("The row is ", row)
            print(row[idx])
            if type(row[idx]) is not type(col):
                try:
                    if (int(row[idx]) or float(row[idx])) and (int(col) or float(col)):
                        print("Index is ", row[idx])
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
        return create_dictionary(consol_list[0], sorted_list)
    else:
        headers = list(range(1, len(consol_list[0]) + 1))
        return create_dictionary(headers, consol_list)


def validate_headers(file_dictionary, column_name):
    """ Validates if the column name does exist """
    try:
        return np.array(file_dictionary[column_name])
    except KeyError as e:
        raise e
    except Exception as ex:
        raise ex


def perform_statistical_computations(file_dictionary, column_name, values):
    """ Validates if the column name does exist """
    print("The minimum value of {} column is {}".format(column_name, np.amin(values)))
    print("The maximum value of {} column is {}".format(column_name, np.amax(values)))
    print("The mean of {} column is {}".format(column_name, np.mean(values)))
    print("The standard deviation of {} column is {}".format(column_name, np.std(values)))
    print("The length of value is {}".format(len(values)))
    print("The list of value is {}".format(list(set(file_dictionary[column_name]))))
    number_of_rows = len(values)
    unique_elements, inverse, counts = np.unique(values, return_inverse='true', return_counts='true')
    print("The array is {}".format(len(unique_elements)))
    assert len(unique_elements) == len(
        list(set(file_dictionary[column_name]))), "The duplicates weren't eliminated properly by numpy."
    if (float(len(unique_elements)) / float(number_of_rows)) * 100 > 30.0:
        print("Data is continuous")
    else:
        print("Data is discrete")


def interpolate_columns(column_1, column_2, column_1_value, file_dictionary):
    validate_headers(file_dictionary, column_1)
    validate_headers(file_dictionary, column_2)
    column_1_array = np.array(file_dictionary[column_1])
    column_2_array = np.array(file_dictionary[column_2])
    if min(column_1_array) <= float(column_1_value) <= max(column_1_array):
        print("Value within range")
    else:
        exit("Value " + str(column_1_value) + " out of range for " + column_1 + "column!Use --summary argument "
                                                                                "instead")
    interpolated_value = np.interp(column_1_value, column_1_array, column_2_array)
    print("The corresponding value of {} for {} with a value {} is {}".format(column_2, column_1, column_1_value, interpolated_value))

    if len(set(file_dictionary[column_2])) < 6 or len(set(file_dictionary[column_1])) < 6:
        exit("Exiting the interpolation as the number of unique data points would be less than 6")
    graph.ylabel(column_2)
    graph.xlabel(column_1)

    # x = np.array(file_dictionary[column_1])
    # y = np.array(file_dictionary[column_2])
    # yinterpol = np.interp(column_1_value, np.array(file_dictionary[column_1]), np.array(file_dictionary[column_2]))
    #yvals = np.linspace(min(column_2_array), max(column_2_array), len(column_2_array))
    #yinterpol = sci_ip.interp1d(0.5, column_1_array, column_2_array)
    #linear = np.polyfit(column_1_value, column_1_value, 1)
    #print("F Order is {}".format(linear))
    # linear = np.polyfit(first_order, column_2_array, 1)
    # degree_2 = np.polyfit(column_1_array, column_2_array, 2)
    # degree_3 = np.polyfit(column_1_array, column_2_array, 3)
    degree_4 = np.polyfit(column_1_array, column_2_array, 4)
    #yp = np.linspace(min(column_2_array), max(column_2_array), len(column_2_array) // 2)
    # graph.plot(column_1_array, column_2_array, '.')
    # graph.plot(yp, np.polyval(linear, first_order), 'g--', label='linear')
    # graph.plot(yp, np.polyval(degree_2, yp), 'c--', label='square')
    # graph.plot(yp, np.polyval(degree_3, yp), 'y--', label='cubic')
    # graph.show()
    #first_order = sci_ip.interp1d(column_1_array, column_2_array)
    #second_order = sci_ip.interp1d(column_1_array, column_2_array, kind='square')
    #third_order = sci_ip.interp1d(column_1_array, column_2_array, kind='cubic')
    # xp = np.linspace(min(x), max(x), len(x) // 2)
    # graph.plot(x, y, '.')
    # graph.plot(xp, yinterpol, 'g--', label='linear')
    # graph.show()
    # graph.plot(xp, np.polyval(linear, xp), 'g--', label='linear')


def create_dictionary(headers, sorted_list):
    for column_id, header in enumerate(headers):
        file_dictionary[header] = []
        for rows in sorted_list:
            file_dictionary[header] += [rows[column_id]]
    return file_dictionary


def plot_graphs(file_dictionary):
    size = len(file_dictionary.keys())
    graph.subplots(size, size, figsize=(80, 80))
    graph.rcParams.update({'font.size': 8})
    for column_1_index, column_1 in enumerate(file_dictionary.keys()):
        for column_2_index, column_2 in enumerate(file_dictionary.keys()):
            graph.xlabel(column_1)
            graph.ylabel(column_2)
            x = np.array(file_dictionary[column_1])
            y = np.array(file_dictionary[column_2])
            linear = np.polyfit(x, y, 1)
            degree_2 = np.polyfit(x, y, 2)
            degree_3 = np.polyfit(x, y, 3)
            degree_4 = np.polyfit(x, y, 4)
            xp = np.linspace(min(x), max(x), len(x) // 2)
            graph.subplot2grid(shape=(size, size), loc=(column_1_index, column_2_index))
            graph.plot(x, y, '.')
            graph.plot(xp, np.polyval(linear, xp), 'g--', label='linear')
            graph.plot(xp, np.polyval(degree_2, xp), 'c--', label='square')
            graph.plot(xp, np.polyval(degree_3, xp), 'y--', label='cubic')
            graph.plot(xp, np.polyval(degree_4, xp), 'm--', label='quadra')
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
    if input_file[2] is not None:
        plot_graphs(file_dictionary)
    elif input_file[3] is not None:
        column_values = validate_headers(file_dictionary, input_file[3])
        perform_statistical_computations(file_dictionary, input_file[3], column_values)
        interpolate_columns(input_file[4][0], input_file[4][1], input_file[4][2], file_dictionary)


if __name__ == "__main__":
    main()

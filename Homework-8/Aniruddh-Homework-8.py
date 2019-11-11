import argparse
import os.path
import csv
import matplotlib.pyplot as graph
import numpy as np

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
        ignored_lines = []
        for line in csv_reader:
            newline = []
            try:
                IND = list(line)
                EX = IND.index('?')
                if EX is not None:
                    ignored_lines.append(line)
            except:
                for value in line:
                    if set_data_type(value) is not None:
                        newline += [set_data_type(value)]
                if len(newline) > 0:
                    refined_list.append(newline)
    return refined_list, ignored_lines


def determine_header_presence(list_of_values):
    """ This function determines the presence of a header by validating the data type of the first column with that
    of the subsequent columns """
    for idx, col in enumerate(list_of_values[0]):
        for row in list_of_values:
            if type(row[idx]) is not type(col):
                try:
                    if (int(row[idx]) or float(row[idx])) and (int(col) or float(col)):
                        pass
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
        print("The column name is incorrect")
        exit(0)
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
    if type(set_data_type(column_1_value)) is str:
        print("Please enter float value or int value for the column value")
        exit(0)

    if min(column_1_array) <= float(column_1_value) <= max(column_1_array):
        print("Value within range")
    else:
        print("Value " + str(column_1_value) + " out of range for " + column_1 + "column!Use --summary argument "
                                                                                "instead")
        exit(0)

    if len(set(file_dictionary[column_2])) < 3 or len(set(file_dictionary[column_1])) < 3:
        print("Exiting the interpolation as the number of unique data points would be less than 6")
        exit(0)

    interpolated_value = np.interp(set_data_type(column_1_value), column_1_array, column_2_array)
    print("The corresponding value of {} for {} with a value {} is {}".format(column_2, column_1, column_1_value, interpolated_value))

    linear = np.polyfit(file_dictionary[column_1], file_dictionary[column_2], 1)
    interpol_linear = np.polyval(linear, set_data_type(column_1_value))
    print("Value for linear equation is {}".format(interpol_linear))

    square = np.polyfit(file_dictionary[column_1], file_dictionary[column_2], 2)
    interpol_square = np.polyval(square, set_data_type(column_1_value))
    print("The interpolated value for 2-degree poly is {}".format(interpol_square))

    cubic = np.polyfit(file_dictionary[column_1], file_dictionary[column_2], 3)
    interpol_cubic = np.polyval(cubic, set_data_type(column_1_value))
    print("THe interpolated value for 3-degree poly is {}".format(interpol_cubic))

    quadra = np.polyfit(file_dictionary[column_1], file_dictionary[column_2], 4)
    interpol_quadra= np.polyval(quadra, set_data_type(column_1_value))
    print("The interpolated value for 4-degree poly is {}".format(interpol_quadra))


def create_dictionary(headers, sorted_list):
    for column_id, header in enumerate(headers):
        file_dictionary[header] = []
        for rows in sorted_list:
            file_dictionary[header] += [rows[column_id]]
    return file_dictionary


def plot_graphs(file_dictionary, column_1, column_2):

    graph.xlabel(column_1)
    graph.ylabel(column_2)
    x = file_dictionary[column_1]
    y = file_dictionary[column_2]
    size = []
    for value in file_dictionary['Single_Epithelial_Cell_Size']:
        size.append(value**2.5)
    color=file_dictionary['Class']
    xp = np.linspace(min(x), max(x), len(x))
    graph.title("{0} x {1}".format(column_1, column_2))
    graph.scatter(x, y, marker='o', c=color, label='Violet - benign, Yellow - Malignant')
    graph.legend(loc='upper left')
    graph.show()


    graph.title("{0} x {1}".format('Bland_Chromatin', 'Single_Epithelial_Cell_Size'))
    graph.xlabel('Bland_Chromatin')
    graph.ylabel('Single_Epithelial_Cell_Size')
    graph.scatter(file_dictionary['Bland_Chromatin'], file_dictionary['Single_Epithelial_Cell_Size'],
                   marker='D', c=color, label='Violet - benign, Yellow - Malignant')

    graph.legend(loc='upper left')
    graph.show()

    graph.title("{0} x {1}".format('Uniformity_of_Cell_Shape', 'Bare_Nuclei'))
    graph.xlabel('Uniformity_of_Cell_Shape')
    graph.ylabel('Bare_Nuclei')
    graph.scatter(file_dictionary['Uniformity_of_Cell_Shape'], file_dictionary['Bare_Nuclei'],
                   marker='D', s=size, c=color, label='Size - Epithial Cell Size, Violet - benign, Yellow - Malignant')
    graph.legend(loc='upper left')
    graph.show()

def main():
    input_file = parser_function()
    refined_list_of_values, ignored_lines = parse_file(input_file[0], input_file[1])
    print("The ignored data is {}".format(ignored_lines))
    header = determine_header_presence(refined_list_of_values)
    file_dictionary = set_headers(refined_list_of_values, header)
    plot_graphs(file_dictionary, "Clump_Thickness", "Uniformity_of_Cell_Size")

if __name__ == "__main__":
    main()

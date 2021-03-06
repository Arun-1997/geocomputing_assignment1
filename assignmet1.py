'''
The following python code has been updated as part of the first assignment for the course Scientific Geocomputing
Done by: Practical group: Anna Arora (S2667312) and Arun Vishwanath Venugopal (S2516306)
Submission date : December 3, 2021
'''

import os
import sys
import csv
from datetime import datetime
import math

try:
    import numpy as np
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print("Modules Numpy or matplotlib are not installed. Kindly check and install.")

############# Task 1  ############


# 1.1

# Relative Path of the data file
data_filepath = 'data/surveyed_trees.csv'

if not os.path.exists(data_filepath):
    raise FileNotFoundError('File not found in this path :' + os.path.abspath(data_filepath))

# 1.2


l_csv_file = open(data_filepath)
csv_reader = csv.DictReader(l_csv_file, delimiter=';')

# Get the field names from csv in lowercase
csv_fieldnames = list()
for i_fldname in csv_reader.fieldnames:
    csv_fieldnames.append(i_fldname.lower())

# Declaring the field names and data type required
l_objectid = ['objectid', int]
l_treelongitude = ['treelongitude', float]
l_treelatitude = ['treelatitude', float]
l_centerlatitude = ['centerlatitude', float]
l_centerlongitude = ['centerlongitude', float]
l_dbh = ['dbh', int]
l_species = ['species', int]
l_creationdate = ['creationdate', str]

# Add the field names in a list and check whether they are available in the csv file
l_filtered_fields = [
    l_objectid, l_treelatitude, l_treelongitude,
    l_centerlatitude, l_centerlongitude, l_dbh,
    l_species, l_creationdate]

# Looping over the list and if provided field is not avaiable, exiting the code.
for i_field in l_filtered_fields:
    if i_field[0] not in csv_fieldnames:
        print(f'Field \'{i_field[0]}\' not available in the data file. Please check the input data')
        sys.exit()

survey_data_dict = dict()
# Make a dictionary with the required fields and object id  value as key
for i_record in csv_reader:
    l_temp_dict = dict()
    l_objid = None
    for j_field in l_filtered_fields:
        l_convert_to_type = j_field[1]
        l_field_name = j_field[0]
        # Check if the field name is object id, then get the value for the survey_data_dict
        # else add the values to l_temp_dict with key as field name and value from the csv file
        # converted from string to the required data type
        if l_field_name == 'objectid':
            l_objid = l_convert_to_type(i_record[l_field_name])
        else:
            l_temp_dict[l_field_name] = l_convert_to_type(i_record[l_field_name])

    survey_data_dict[l_objid] = l_temp_dict

# Close the csv file
l_csv_file.close()


# print(survey_data_dict)


############# Task 2  ############
# 2.1
def get_roadside_by_date(creation_date):
    '''
    :created date: December 1, 2021
    :purpose: This function determines the roadside using the survey date of the trees
    :param creation_date: String format
    :return: String with possible values : 'N/W' , 'S/E', 'Invalid'
    '''

    NW_dates = (13, 14, 23)
    SE_dates = (20, 21, 22)
    try:
        # checking the format of datetime and returning it as an object
        date_time_obj = datetime.strptime(creation_date, '%m/%d/%Y %H:%M')
        creation_day = date_time_obj.day  # extracting the day
        output = 'None'
        if creation_day in NW_dates:  # checking if it belongs to N/W data collection
            output = 'N/W'
        elif creation_day in SE_dates:  # checking if it belongs to S/E data collection
            output = 'S/E'
        return output

    except ValueError:
        output = 'Invalid'  # If the date format is incorrect
        return output


# 2.2


def get_roadside_by_coord(tree_coord, center_coord):
    '''
    :created date: December 1, 2021
    :purpose: This function determines the roadside using the difference in coordinates.
    :param tree_coord: Coordinates of the false tree location as a list or tuple
    :param center_coord: Coordinates of the position on the centerline nearest to false tree location as a list or tuple
    :return: String with possible values : 'N/W' , 'S/E'
    '''

    diff_vector = [tree_coord[0] - center_coord[0],
                   tree_coord[1] - center_coord[1]]  # difference between coordinates to determine the position

    if diff_vector[0] < diff_vector[1]:
        return 'N/W'  # difference in longitudes is less than latitudes
    else:
        return 'S/E'


# 2.3
# Testing of the two functions created in Task 2
print('Test 1 for Function 1 with input date : 11/13/2021 12:43 - ', get_roadside_by_date('11/13/2021 12:43'))
print('Test 2 for Function 1 with input date : 2021/11/13 12:43 - ', get_roadside_by_date('2021/11/13 12:43'))
print('Test 1 for Function 2 with input coordinates : [0,0] , [10, -10] - ', get_roadside_by_coord([0, 0], [10, -10]))
print('Test 2 for Function 2 with input coordinates : [0,0] , [-10, 10] - ', get_roadside_by_coord([0, 0], [-10, 10]))


############# Task 3  ############

trees_positioned_at_wrong_side_of_road = []
trees_with_false_positions = []

for i_key, j_val in survey_data_dict.items():
    l_checkdate = j_val['creationdate']
    l_tree_coord = [j_val['treelongitude'], j_val['treelatitude']]  # List of tree coordinates from data
    l_center_coord = [j_val['centerlongitude'], j_val['centerlatitude']]  # List of center coordinates from data

    # 3.1 Getting location of tree using roadside by date value by passing date to the function below
    j_val['roadsidebydate'] = get_roadside_by_date(l_checkdate)

    # 3.2 Getting roadside by coordinate value by passing tree coordinates and center coordinates to the method below
    j_val['roadsidebycoord'] = get_roadside_by_coord(l_tree_coord, l_center_coord)

    # 3.3 Comparing roadsidebydate and roadsidebycoord and assigning it to a boolean value
    l_bool = (j_val['roadsidebydate'] == j_val['roadsidebycoord'])
    j_val['isatcorrectsideofroad'] = l_bool

    # 3.4 list of objectids for trees with false positions
    trees_with_false_positions.append(i_key)
    # 3.4 list of objectids for trees positioned at the wrong side of the road
    if not l_bool:
        trees_positioned_at_wrong_side_of_road.append(i_key)
print(
    f'The count for trees with false positions : {len(trees_with_false_positions)}')
print(
    f'The count for trees that are positioned at the wrong side of the road : {len(trees_positioned_at_wrong_side_of_road)}')


############# Task 4  ############
# 4.1

def st_translate(current_tree_coord, displacement, angle):
    '''
    :purpose Convert false tree coordinates to true tree coordinates
    :param current_tree_coord: False tree coordinates recorded during the survey
    :param displacement: displacement between the tree and the position where coordinates were calculated
    :param angle: angle between the road and the tree
    :return: true coordinates of the tree
    '''

    x = current_tree_coord[0]
    y = current_tree_coord[1]
    x += displacement * math.cos(angle)  # Calculating the true longitude
    y += displacement * math.sin(angle)  # Calculating the true latitude
    return [x, y]


# 4.2, 4.3, 4.4

# Looping over the list of objectids with trees that has false positions.
# As mentioned in the project description, all tree coordinates were collected at false positions
for objectid in trees_with_false_positions:
    item = survey_data_dict[objectid]
    tree_coord = [item["treelongitude"], item["treelatitude"]]
    center_coord = [item["centerlongitude"], item["centerlatitude"]]

    # difference between coordinates to determine the angle between centre location and tree location used for calculation
    diff_vector = [tree_coord[0] - center_coord[0],
                   tree_coord[1] - center_coord[1]]


    tree_angle = math.atan2(diff_vector[1], diff_vector[0])

    displacement = 2.0 + 3.25 * item["dbh"] / 200  # distance between the survey point and the centre of tree
    # 2 m - telescopic pole length, 32.5 cm - pole segment length, dbh - diameter at breast height in 1/10 of segment

    # Changing the displacement sign if the survey shows wrong side of the tree location
    if not item['isatcorrectsideofroad']:
        displacement = -displacement

    # calling the translate function to retrieve the true coordinates
    true_tree_coord = st_translate(tree_coord, displacement, tree_angle)

    item['truetreelongitude'] = true_tree_coord[0]  # updating the survey data dictionary with true coordinates
    item['truetreelatitude'] = true_tree_coord[1]

# 4.5
# Writing the survey data into a csv file

try:
    labels = ['objectid'] + list(survey_data_dict[1].keys())  # extracting the header information

    # creating a new csv file and writing the survey data
    with open('trees_true_positions.csv', 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=labels)
        writer.writeheader()
        for objectid, elem in survey_data_dict.items():
            elem['objectid'] = objectid
            writer.writerow(elem)

except IOError:
    print("I/O error")

finally:
    f_out.close()

############# Task 5  ############

# 5.1, 5.2

# Loading the data csv as matrix with columns. Getting the column index from the data file
col_index = tuple([csv_fieldnames.index('objectid'), csv_fieldnames.index('species'), csv_fieldnames.index('dbh')])
matrix = np.loadtxt(data_filepath, delimiter=';', skiprows=1, usecols=col_index)

# 5.3

# Getting beech species as True
indx_of_beech = matrix[:, 1] == 1

# Getting oak species as True
indx_of_oak = matrix[:, 1] == 0

# Getting list of Diameter at breast height (dbh) for beech 
beech_diameter = matrix[indx_of_beech, 2]

# Getting list of Diameter at breast height (dbh) for oak
oak_diameter = matrix[indx_of_oak, 2]

# 5.4
# Printing the statistics of beech and oak trees diameters

print("Beech tree statistics")
print("N : ", len(beech_diameter), ",  Minimum : ", np.min(beech_diameter), " , Maximum : ", np.max(beech_diameter),
      " , Mean : ", np.mean(beech_diameter))
print("Oak tree statistics")
print("N : ", len(oak_diameter), ",  Minimum : ", np.min(oak_diameter), " , Maximum : ", np.max(oak_diameter),
      " , Mean : ", np.mean(oak_diameter))

# 5.5

# Plot the subplot 1 by 2. Row 1 and column 1 here
plt.subplot(1, 2, 1)

# Histogram for beech  tree diameter
plt.hist(beech_diameter, bins=10, color='brown')
plt.xlabel('Tree Diameter (dbh)')  # X and Y labels for Tree Diameter and count
plt.ylabel('Count')
plt.title('Beech Tree diameters')  # Title for beech tree diameters
plt.subplot(1, 2, 2)

# Histogram for oak tree diameter
plt.hist(oak_diameter, bins=10, color='brown')
plt.xlabel('Tree Diameter (dbh)')
plt.ylabel('Count')
plt.title('Oak Tree diameters')  # Title for oak tree diameters
plt.show()


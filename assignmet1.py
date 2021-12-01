############# Task 1  ############
import os,sys
import csv

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
l_objectid = ['objectid',int]
l_treelongitude = ['treelongitude',float]
l_treelatitude = ['treelatitude',float]
l_centerlatitude = ['centerlatitude',float]
l_centerlongitude = ['centerlongitude',float]
l_dbh = ['dbh',int]
l_species = ['species',int]
l_creationdate = ['creationdate',str]

# Add the field names in a list and check whether they are available in the csv file
l_filtered_fields =[l_objectid,l_treelatitude,l_treelongitude,l_centerlatitude,l_centerlongitude,l_dbh,l_species,l_creationdate]

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


# print(survey_data_dict)


############# Task 2  ############
from datetime import datetime
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
        date_time_obj = datetime.strptime(creation_date, '%m/%d/%Y %H:%M')    #checking the format of datetime and returning it as an object
        creation_day = date_time_obj.day    #extracting the day
        output = 'None'
        if creation_day in NW_dates:        #checking if it belongs to N/W data collection
            output = 'N/W'
        elif creation_day in SE_dates:      #checking if it belongs to S/E data collection
            output = 'S/E'
        return output
    except ValueError:
        output = 'Invalid'          #If the date format is incorrect
        return output
    


# 2.2


def get_roadside_by_coord(tree_coord, center_coord):
    '''
    :created date: December 1, 2021
    :purpose: This function determines the roadside using the difference in coordinates.
    :param tree_coord: Coordinates of the false tree location as a list or tuple
    :param center_coord: Coordinates of the position on the centerline nearest to the false tree location
    :return: String with possible values : 'N/W' , 'S/E'
    '''
    diff_vector = [tree_coord[0] - center_coord[0],
                   tree_coord[1] - center_coord[1]]     # difference between coordinates to determine the position

    if diff_vector[0] < diff_vector[1]:
        return 'N/W'    #difference in longitudes is less than latitudes
    else:
        return 'S/E'


# 2.3


# ############# Task 3  ############



trees_positioned_at_wrong_side_of_road = []


for i_key,j_val in survey_data_dict.items():
    l_checkdate = j_val['creationdate']
    l_tree_coord = [j_val['treelongitude'],j_val['treelatitude']]         # List of tree coordinates from data
    l_center_coord = [j_val['centerlongitude'],j_val['centerlatitude']]   # List of center coordinates from data
    # 3.1 Getting roadside by date value by passing date to the method below
    j_val['roadsidebydate'] = get_roadside_by_date(l_checkdate)
    # 3.2 Getting roadside by coordinate value by passing tree coordinates and center coordintaes to the method below
    j_val['roadsidebycoord'] = get_roadside_by_coord(l_tree_coord,l_center_coord)
    # 3.3 Comparing roadsidebydate and roadsidebycoord and assigning it to a boolean value
    l_bool = (j_val['roadsidebydate'] == j_val['roadsidebycoord'])
    j_val['isatcorrectsideofroad'] = l_bool
    # 3.4 list of objectids for trees with false positions
    if not l_bool:
        trees_positioned_at_wrong_side_of_road.append(i_key)

print(f'The count for trees that are positioned at the wrong side of the road : {len(trees_positioned_at_wrong_side_of_road)}')




# ############# Task 4  ############
# # 4.1

# def st_translate(current_tree_coord, displacement, angle):
#     x = current_tree_coord[0]
#     y = current_tree_coord[1]
#     x += displacement * math.cos(angle)
#     y += displacement * math.sin(angle)
#     return [x, y]


# # 4.2, 4.3, 4.4

# for objectid, item in survey_data_dict:
#     tree_coord = [item["treelongitude"], item["treelatitude"]]

#     diff_vector = []

#     tree_angle = math.atan2(diff_vector[1], diff_vector[0])

#     displacement = 2.0 + 3.25 * item["dbh"]/200

#     if not item["isatcorrectsideofroad"]:
#         displacement = -displacement

#     true_tree_coord = st_translate()



# # 4.5

# try:
#     labels = ['objectid'] + list(survey_data_dict[1].keys())
#     with open('trees_true_positions.csv', 'r') as f_out:
#         writer = csv.DictReader(f_out, fieldnames=labels)
#         writer.writeheader()
#         for objectid, elem in survey_data_dict.items():


# except IOError:
#     print("I/O error")

# ############# Task 5  ############

# # 5.1, 5.2
# matrix = np.loadtxt()

# # 5.3
# indx_of_beech = matrix[:, 1] == 1
# indx_of_oak = matrix[:, 1] == 0

# beech_diameter = matrix
# oak_diameter = matrix

# # 5.4
# print("Beech tree statistics")
# print("N : ", , ",  Minimum : ", , " , Maximum : ", , " , Mean : ", )
# print("Oak tree statistics")
# print("N : ", , ",  Minimum : ", , " , Maximum : ", , " , Mean : ", )


# # 5.5


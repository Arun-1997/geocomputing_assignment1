############# Task 1  ############
#test
#anothertest
#test1
import os

#testing
# 1.1

data_filepath = "data/data-trees.csv"


if file_not_exist:
    raise FileNotFoundError(
        "File not found in this path :" + os.path.abspath(data_filepath))


# 1.2
survey_data_dict = dict()

with open(data_filepath) as file:
    csv_reader = csv.DictReader(file, delimiter=',')


############# Task 2  ############

# 2.1
def get_roadside_by_date(creation_date):
    pass


# 2.2


def get_roadside_by_coord(tree_coord, center_coord):
    diff_vector = [tree_coord[0] - center_coord[0],
                   tree_coord[1] - center_coord[1]]

    if diff_vector[0] < diff_vector[1]:
        return "N/W"
    else:
        return "S/E"


# 2.3


############# Task 3  ############

# 3.1, 3.2. 3.3


# list of objectids for trees with false positions

# 3.4
trees_positioned_at_wrong_side_of_road = []


############# Task 4  ############
# 4.1

def st_translate(current_tree_coord, displacement, angle):
    x = current_tree_coord[0]
    y = current_tree_coord[1]
    x += displacement * math.cos(angle)
    y += displacement * math.sin(angle)
    return [x, y]


# 4.2, 4.3, 4.4

for objectid, item in survey_data_dict:
    tree_coord = [item["treelongitude"], item["treelatitude"]]

    diff_vector = []

    tree_angle = math.atan2(diff_vector[1], diff_vector[0])

    displacement = 2.0 + 3.25 * item["dbh"]/200

    if not item["isatcorrectsideofroad"]:
        displacement = -displacement

    true_tree_coord = st_translate()


# 4.5

try:
    labels = ['objectid'] + list(survey_data_dict[1].keys())
    with open('trees_true_positions.csv', 'r') as f_out:
        writer = csv.DictReader(f_out, fieldnames=labels)
        writer.writeheader()
        for objectid, elem in survey_data_dict.items():


except IOError:
    print("I/O error")

############# Task 5  ############

# 5.1, 5.2
matrix = np.loadtxt()

# 5.3
indx_of_beech = matrix[:, 1] == 1
indx_of_oak = matrix[:, 1] == 0

beech_diameter = matrix
oak_diameter = matrix

# 5.4
print("Beech tree statistics")
print("N : ", , ",  Minimum : ", , " , Maximum : ", , " , Mean : ", )
print("Oak tree statistics")
print("N : ", , ",  Minimum : ", , " , Maximum : ", , " , Mean : ", )


# 5.5
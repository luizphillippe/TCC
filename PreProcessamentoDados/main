STATIONARY_TIME = 10

from manipulating_PLD_MET_data import *
from manipulate_files import find_PLD_file_wrong_name, correct_PLD_file_name, get_PLD_group, get_PLD_case
import pathlib
import pandas as pd

# 1. Find all met and pld files in the directory
data_folder = pathlib.Path(r"C:\Users\LUIMAR\Desktop\TCC test\Dados")

met_files = list(data_folder.glob('**/*.MET'))
pld_files = list(data_folder.glob('**/*.PLD'))

# 2. Find PLD files that do not have the C1 in the name
wrong_name_files = find_PLD_file_wrong_name(pld_files)

# 3. Correct the PLD file name
for file in wrong_name_files:
    new_file_path = correct_PLD_file_name(file)
    file.rename(new_file_path)

# 4. Get heave, mean, group and case from PLD files
surge_mean_list = []
sway_mean_list = []
pld_group_list = []
pld_case_list = []

for file in pld_files:
    # get the mean of the surge and sway data above 10 seconds to avoid the transient
    pld_df = parse_pld_file_to_dataframe(file)
    surge_mean, sway_mean = surge_sway_data_mean(pld_df, above_time=STATIONARY_TIME)

    surge_mean_list.append(surge_mean)
    sway_mean_list.append(sway_mean)

    # Get the group and name of the PLD file
    pld_group_list.append(get_PLD_group(file))
    pld_case_list.append(get_PLD_case(file))

# Store the data into a dataframe
motion_data = pd.DataFrame({'surge_mean': surge_mean_list, 'sway_mean': sway_mean_list, 'group': pld_group_list, 'case': pld_case_list})

# 5. Concatenate all the met data and filter VVEL, VDIR, HS1, TP1, DIR1, CVEL0, CDIR0 columns. Add group and case collumns too
met_df_list = [filter_met_data(met_file) for met_file in met_files]

# concatenate the met data 
enviroment_data = pd.concat(met_df_list, axis=0, ignore_index=True)

# 6. Clear empty rows
enviroment_data = clear_empty_rows(enviroment_data)
motion_data = clear_empty_rows(motion_data)

# 7. Sort the motion data by group and case to match with pld
motion_data = motion_data.sort_values(by=['group', 'case'], ignore_index=True)

# 8. Check if the motion data and met data have the group and case columns in the same order
if not motion_data['group'].equals(enviroment_data['group']) or not motion_data['case'].equals(enviroment_data['case']):
    raise Exception('The motion data and met data do not have the group and case columns in the same order')

# 8. Drop the group and case columns from the motion data and for the met data
motion_data.drop(['group', 'case'], axis=1, inplace=True)
enviroment_data.drop(['group', 'case'], axis=1, inplace=True)

# 8. Concatenate the motion data with the met data
all_data = pd.concat([motion_data, enviroment_data], axis=1)

# 7. Save the data into a json file, considering the first two columns as the outputs and the rest as the inputs



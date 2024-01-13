from typing import List
import pathlib

def find_PLD_file_wrong_name(met_files: List[pathlib.Path]) -> List[pathlib.Path]:
    # find PLD files that do not have the C1 in the name
    wrong_name_files = []
    for file in met_files:
        file_name = file.name

        if len(file_name.split('_')) > 3:
            continue
        
        wrong_name_files.append(file)

    return wrong_name_files


def correct_PLD_file_name(wrong_file_path):
    # correct the PLD file name
    root = wrong_file_path.parent

    wrong_file_name = wrong_file_path.name

    file_name_parts = wrong_file_name.split('_')

    if len(file_name_parts) == 3:
        file_name_parts.insert(1, 'C1')
        new_file_name = '_'.join(file_name_parts)

        return pathlib.Path(root,new_file_name)

    return wrong_file_path

def get_PLD_group(pld_path : pathlib.Path) -> int:
    file_name = pld_path.name
    file_name_parts = file_name.split('_')

    # file name is in the form of Wind-1_C100_d_UF1.PLD, so the group is the last character of the first part
    group = int(file_name_parts[0][-1])

    return group

def get_PLD_case(pld_path : pathlib.Path) -> int:
    file_name = pld_path.name
    file_name_parts = file_name.split('_')

    # file name is in the form of Wind-1_C100_d_UF1.PLD, so the case is the second part
    case = file_name_parts[1]

    case_num = int(case.replace('C', ''))

    return case_num

def get_met_group(met_path : pathlib.Path):
    file_name = met_path.name
    file_name_parts = file_name.split('_')

    # file name is in the form of conjunto2_jun2-1.met, so the group is the 5th last character of the second part
    group = int(file_name_parts[1][-5])

    return group
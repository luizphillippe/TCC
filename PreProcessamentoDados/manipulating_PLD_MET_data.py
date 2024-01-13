import pandas as pd
import numpy as np
from PreProcessamentoDados.manipulate_files import get_met_group

'''
This script is used to parse the PLD and MET files into a pandas dataframe.

'''


def parse_pld_file_to_dataframe(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r') as f:
        lines = f.readlines()

     # Remove the first 3 lines
    lines = lines[3:]

    # Removing unnecessary spaces and newlines
    lines = [line for line in lines]

    # Splitting the data into columns
    data = [line.split() for line in lines]

    # Data is in the form of TIME  WAVE-EL | WIND | SURGE | SWAY | HEAVE | ROLL | PITCH | YAW | DRIFT | ANG
    named_columns = ['TIME', 'WAVE-EL', 'WIND', 'SURGE',
                     'SWAY', 'HEAVE', 'ROLL', 'PITCH', 'YAW', 'DRIFT', 'ANG']

    unamed_columns = [None] * (len(data[0]) - len(named_columns))

    df = pd.DataFrame(data, columns=named_columns + unamed_columns)

    return df


def parse_met_file_to_dataframe(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Remove the first 19 lines
    lines = lines[19:]

    # Removing unnecessary spaces and newlines
    lines = [line for line in lines]

    # Splitting the data into columns
    data = [line.split() for line in lines]

    # Data is in the form of data_hora  data_hora         VVEL    VDIR   HSTOT     HS1      TP1   DIR1    HS2     TP2    DIR2    CVEL0    CDIR0
    df = pd.DataFrame(data)

    # get the first row for the header and remove index 0
    new_header = df.iloc[0].tolist()

    # splitting the data_hora column into two columns
    new_header = new_header[1:-1]

    # take the data less the header row
    df = df[1:]

    # drop the first two columns
    df = df.drop(df.columns[[0, 1]], axis=1)

    # set the header row as the df header
    df.columns = new_header

    # reset index values
    df.reset_index(drop=True, inplace=True)

    return df


def surge_sway_data_mean(met_df: pd.DataFrame, above_time: float = 0) -> tuple[float, float]:
    '''
    This function calculates the mean of the surge and sway columns of the pld dataframe.
    :param met_df: dataframe with the met data
    :param above_time: time in seconds to filter values above

    '''

    # filtering the data_hora column to get only the values above the above_time

    data_abv_time = met_df[met_df['TIME'].astype(float) >= above_time]

    # convert the data_hora column to datetime

    surge_mean = data_abv_time['SURGE'].astype(float).mean()
    sway_mean = data_abv_time['SWAY'].astype(float).mean()

    return surge_mean, sway_mean

def filter_met_data(met_file_path):
    met_df = parse_met_file_to_dataframe(met_file_path)

    num_rows = met_df.shape[0]

    # get the group of the met file
    group = int(get_met_group(met_file_path))
    group_list = [group] * num_rows

    # list of cases
    cases_lits = list(range(1, num_rows+ 1))

    # get the VVEL, VDIR, HS1, TP1, DIR1, CVEL0, CDIR0 columns
    met_df = met_df[['VVEL', 'VDIR', 'HS1', 'TP1', 'DIR1', 'CVEL0', 'CDIR0']]

    # add the group and case columns
    met_df['group'] = group_list
    met_df['case'] = cases_lits

    return met_df

def clear_empty_rows(df):
    # Create a copy of the DataFrame to avoid modifying the original one
    df = df.copy()

    # change the empty values to NaN
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    # drop rows with empty values
    df.dropna(inplace=True)

    # reset index values
    df.reset_index(drop=True, inplace=True)

    return df


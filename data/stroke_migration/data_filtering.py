import pandas as pd
from datetime import datetime
import argparse


def is_time_diff_below_threshold(date1, date2, threshold=30):
    return abs((date1 - date2).total_seconds()) / 60 < threshold


def clean_up(input_data: pd.DataFrame):
    output_data = input_data
    data_len = len(output_data.index)
    for i in range(1, data_len-1):
        if i % 10000 == 0 and i != 0:
            print(datetime.now(), data_len - i, 'left...')
        if is_time_diff_below_threshold(output_data.at[i, 'previous_date'], output_data.at[i, 'date']):
            new_previous_date = output_data.at[i, 'previous_date']
            output_data.at[i + 1, 'previous_date'] = new_previous_date
            output_data = output_data.drop([i], axis=0)
    return output_data


'''
Arguments
'''

parser = argparse.ArgumentParser(description='Arguments.')
parser.add_argument(
    'input_file',
    type=str
)
parser.add_argument(
    'output_file',
    type=str
)

args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file

FORMAT = '%Y-%m-%d %H:%M:%S.%f'

data = pd.read_csv(input_file)

data['date'] = data['date'].apply(lambda date: datetime.strptime(date, FORMAT))
data = data.sort_values('date')
data = data.drop(['Unnamed: 0'], axis=1)
data = data.reset_index(drop=True)
data['previous_date'] = data['date'].shift()

print(datetime.now(), 'Starting')

cleaned_data = clean_up(data)

cleaned_data = cleaned_data.drop(['previous_date'], axis=1)
cleaned_data = cleaned_data.reset_index(drop=True)

cleaned_data.to_csv(output_file)

print(datetime.now(), 'Finished')
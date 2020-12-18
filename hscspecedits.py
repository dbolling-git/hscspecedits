import pandas as pd
import numpy as np
import sys
import argparse
from textwrap import dedent
from progress.bar import Bar

#Author: Daryl Bolling
#Date: 2020-12-18
#Email: dbolling4@protonmail.com

parser = argparse.ArgumentParser(description='Count the number of changes in a given time per Editor')
parser.add_argument('-i','--inputfile', type=str,required=True,help='Type name of the input .csv file. If not in current directory specify path.')

parser.add_argument('-st','--start_date',type=str,required=True,help="Enter the start date of the range")
parser.add_argument('-end','--end_date',type=str,required=True,help="Enter the end date of range.")


group = parser.add_mutually_exclusive_group()
parser.add_argument('-s','--saveas',action='store_true',help='Name of the Output file.')
group.add_argument('-e','--editors',action='store_true',help='Number of changes made by Editor.')

args = parser.parse_args()

#if __name__ == '__main__'

def uniqueIndexes(l):
    seen = set()
    res = []
    for i, n in enumerate(l):
        if n not in seen:
            res.append(i)
            seen.add(n)
    return res
try:
    df = pd.read_csv(args.inputfile)
except OSError:
     print(dedent("""
     File not found or incorrect file type. If file not in directory specify path to file.
     """))
     sys.exit(1)


df['timestamp']=df['Timestamp']
# these are the steps to getting the Datetime in the index
datetime_series = pd.to_datetime(df['Timestamp'])
datetime_index = pd.DatetimeIndex(datetime_series.values)
df=df.set_index(datetime_index)
df.drop('Timestamp',axis=1,inplace=True)
df.sort_index(inplace=True)
def cal_dates_start(start):
    factor1 = (start)
    return factor1
def cal_dates_end(end):
    factor2 = (end)
    return factor2
start_time = cal_dates_start(args.start_date)
end_time = cal_dates_end(args.end_date)
try:
    if (start_time == 'start') and (end_time == 'end'):
        pass
    elif (start_time == 'start') and (end_time != 'end'):
        df = df[:end_time]
    elif (start_time != 'start') and (end_time == 'end'):
        df = df[start_time:]
    else:
        df = df[start_time:end_time]

    

except ValueError:
    print("These dates are not in the set")
    exit(1)

df.sort_values(by='occid', inplace=True) #sort all the values by occid number get them in order
occid_list = df['occid'].to_list() #gives all the occid values in order in a list
unique_occid_list = uniqueIndexes(occid_list) #gives us the index numbers of all the occid lists
len_df = len(df)  #length of our dataframe
df.sort_values(by='occid', inplace=True) #sort all the values by occid number get them in order
df['occid'].nunique()
occid_list = df['occid'].to_list() #gives all the occid values in order in a list
unique_occid_list = uniqueIndexes(occid_list) #gives us the index numbers of all the occid lists
len_df = len(df)  #length of our dataframe
comparison_list = np.arange(0, len_df, 1).tolist() #make a list from zero to the length of index
df['index'] = comparison_list #make a new column of these values
df.set_index('index',inplace=True) #set that column as our index values
max_list_length = len(comparison_list)
max_occid_length = len(unique_occid_list)
bar_factor = max_list_length - max_occid_length
with Bar('Processing...', max=bar_factor) as bar:
    for item in comparison_list:         #pull out the unique values delete redundant ones
        if item not in unique_occid_list:
            df.drop(item,axis=0,inplace=True)
            bar.next()
        else:
            pass

df.reset_index(drop="True",inplace=True)
df = df.rename(columns={"timestamp": "Timestamp"})
df = df[['EditId', 'occid', 'dbpk','CatalogNumber', 'ReviewStatus',
         'AppliedStatus','Editor','Timestamp','FieldName','OldValue',
         'NewValue',]]
df=df.set_index('EditId')


print('\n')
if args.editors:
    for idx,name in enumerate(df['Editor'].value_counts().index.tolist()):
  
        print('Name :', name)
        print('Edits:', df['Editor'].value_counts()[idx])
        print('\n')
    #print('\nEditors              Edits Made') #alternate way to display lists
    #print(df['Editor'].value_counts())
    #print('\n')

        #import matplotlib.pyplot as plt #if you want to out a bar graph

        #df['Editor'].value_counts().plot(kind='bar')

        #plt.show()

elif args.saveas:
    output_name = 'Output_'+args.inputfile
    df.to_csv(output_name)
    print('File saved in directory as',output_name)
else:
    pass

import pandas as pd
# import pickle as pckl
import os
import matplotlib.pyplot as plt
import seaborn as sns
import json

def prnt(s=''):
    if s:
        print(s)
    print('='*os.get_terminal_size()[0])

g = 9.81 # N/kg

class specimen():
    def __init__(self, filename, from_dump = False):
        self.filename = filename

        with open(f'param{filename[:-4]}.json', 'r') as file:
            print(f'param{filename[:-4]}.json')
            param = json.load(file)

        trig = float(param['trig'])


        newcols1 = {'Source':'Time/s', 'CH1':'CH1/V'}
        self.df1 = pd.read_csv(self.filename, skiprows=[1], usecols=[0,1]).rename(columns=newcols1)

        newcols2 = {'Source':'Time/s', 'CH2':'CH2/V'}
        self.df2 = pd.read_csv(self.filename, skiprows=[1], usecols=[0,2]).rename(columns=newcols2)

        self.df1['Time/s'] -= self.df1.iloc[0]['Time/s']
        self.df2['Time/s'] -= self.df2.iloc[0]['Time/s']

        self.df1['CH1/V'] -= self.df1[self.df1['Time/s'] < trig]['CH1/V'].mean()
        self.df2['CH2/V'] -= self.df2[self.df2['Time/s'] < trig]['CH2/V'].mean()

        self.df1['CH1/V'] = self.df1['CH1/V'].rolling(50).mean()
        self.df2['CH2/V'] = self.df2['CH2/V'].rolling(50).mean()

        self.df2['Time/s'] += float(param['shft'])


        cut1, cut2 = map(float, param['cut'].split(','))

        self.df1.drop(self.df1[ (self.df1['Time/s'] < cut1) | (self.df1['Time/s'] > cut2) ].index, inplace=True)
        self.df2.drop(self.df2[ (self.df2['Time/s'] < cut1) | (self.df2['Time/s'] > cut2) ].index, inplace=True)

        self.df1['Time/s'] -= self.df1.iloc[0]['Time/s']
        self.df2['Time/s'] -= self.df2.iloc[0]['Time/s']

        self.df1['CH1/V'] -= float(param['zero'])
        self.df2['CH2/V'] -= float(param['zero'])

        self.df1['CH1/MPa'] = self.df1['CH1/V'] * float(param['k']) * g / float(param['S']) / 1e+6
        self.df2['CH2/MPa'] = self.df2['CH2/V'] * float(param['k']) * g / float(param['S']) / 1e+6

        self.df1.reset_index(inplace=True)
        self.df2.reset_index(inplace=True)

        # if from_dump:
        #     with open('dump.pickle', 'rb') as dumpfile:
        #         pckl.load(dumpfile)
        # else:
        #     with open('dump.pickle', 'wb') as dumpfile:
        #         pckl.dump(relaxed_specimens, dumpfile)




filenames = [
    '62kg.csv',
    '95.6kg.csv',
    '99kg.csv',
]

relaxed_specimens = []
for filename in filenames:
    relaxed_specimens.append(specimen(filename=filename))

for i in range(3):
    plt.title(filenames[i])

    plt.hlines(0, relaxed_specimens[i].df1.iloc[0]['Time/s'], relaxed_specimens[i].df1.iloc[-1]['Time/s'], color='r')

    sns.lineplot(
        data=relaxed_specimens[i].df1,
        x = 'Time/s',
        y = 'CH1/MPa',
        label = 'CH1',         
                 )
    sns.lineplot(
        data=relaxed_specimens[i].df2,
        x = 'Time/s',
        y = 'CH2/MPa',
        label = 'CH2',       
                 )
    
   # plt.show()

for i in range(3):
    xldf = pd.DataFrame()
    xldf['Time/s'] = relaxed_specimens[i].df1['Time/s']
    xldf['CH1/MPa'] = relaxed_specimens[i].df1['CH1/MPa']
    xldf['CH2/MPa'] = relaxed_specimens[i].df2['CH2/MPa']
    xldf.to_excel(f"{filenames[i][:-4]}.xlsx") 
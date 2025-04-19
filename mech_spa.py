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

class specimen():
    def __init__(self, filename, from_dump = False):
        self.filename = filename

        with open(f'param{filename[:-4]}.json', 'r') as file:
            print(f'param{filename[:-4]}.json')
            param = json.load(file)

        trig = float(param['trig'])


        newcols = {'Source':'Time/s', 'CH1':'CH1/V', 'CH2':'CH2/V'}
        self.df = pd.read_csv(self.filename, skiprows=[1], usecols=[0,1,2]).rename(columns=newcols)

        self.df['Time/s'] -= self.df.iloc[0]['Time/s']

        self.df['CH1/V'] -= self.df[self.df['Time/s'] < trig]['CH1/V'].mean()
        self.df['CH2/V'] -= self.df[self.df['Time/s'] < trig]['CH2/V'].mean()

        self.df['CH1/V'] = self.df['CH1/V'].rolling(50).mean()
        self.df['CH2/V'] = self.df['CH2/V'].rolling(50).mean()

        self.df['CH2/V'].shift(param['shft'])


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

    prnt()
    print(relaxed_specimens[-1].df.head())

for i in range(3):
    plt.title(filenames[i])
    sns.lineplot(
        data=relaxed_specimens[i].df,
        x = 'Time/s',
        y = 'CH1/V',         
                 )
    sns.lineplot(
        data=relaxed_specimens[i].df,
        x = 'Time/s',
        y = 'CH2/V',         
                 )
    
    plt.show()
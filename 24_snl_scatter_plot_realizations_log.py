# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from math import floor, log10
#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")

#load results from xlsx file into dictionary of dataframes (one dataframe for each xlsx sheet/qoi)
data_folder='./input_output_datasets'
filename='snl_qoi_realizations.xlsx'

filename_prefix=filename.replace(".xlsx","")

# Import data

realization_data = pd.read_excel(os.path.join(data_folder,filename),sheet_name='all')
parameters=list(realization_data.columns[1:9])
qois=list(realization_data.columns[9:])

    
#select qoi
qoi='Peak_TotalI129_M'
#qoi="FractionofSpikeinRepository_1Myr"
#qoi="FractionalMassFluxfromRepo_1Myr"
#qoi="AqEb_RockEb_1Myr"
#qoi="RockAq_RockEb_1Myr"


realization_data_qoi=realization_data[['Realization']+parameters+[qoi]]
realization_data_qoi_melted=realization_data_qoi.melt(id_vars=['Realization', qoi], value_vars=parameters,value_name='parameter_value',var_name='parameter')





# parameters = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']
# # create some dummy test data
# df = pd.DataFrame({'Realization': np.random.choice(['Q1', 'Q2', 'Q3', 'Q4'], 1000),
#                           'Temperature': np.random.randint(-4, 28, 1000),
#                           'MeanEnergy': np.random.uniform(1, 119, 1000)},
#                          index=np.random.choice(parameters, 1000))

# palette = {'Q1': 'tab:blue', 'Q2': 'tab:green', 'Q3': 'tab:orange', 'Q4': 'tab:red'}

# # Convert the index to an real column
# df.index.name = 'parameter'
# df = df.reset_index()


                  
                  
g = sns.lmplot(data=realization_data_qoi_melted, col='parameter', col_wrap=4, height=3, aspect=1,
                x='parameter_value', y=qoi, 
                facet_kws={'sharex': False, 'sharey': True},
                #alpha=0.5,                color='0.8',edgecolor='0.1',
                #palette=palette
                fit_reg=True,ci=None,
                scatter_kws={'alpha':0.25, 'color':'0.8','edgecolor':'0.1'}, line_kws={'color': '#0072B2'}
                )




for axes in g.axes.flat:
    axes.ticklabel_format(axis='both', style='scientific', useMathText=True,scilimits=(0,0))




g.despine(top=False, right=False, left=False, bottom=False, offset=None, trim=False)
#g.set(xlim=(-5, 1))
#g.set(ylim=(0.5*10e-11, 1.5*10e-8))
#g.set(ylim=(4.5*10e-3, 3.5*10e-2))
#g.set(ylim=(5*10e-8, 0.2*10e-6))
g.set(yscale='log')
g.set(xlabel=None)
g.set(ylabel=f"{qoi}")
g.fig.set_size_inches(12,6)
g.fig.tight_layout()



g.savefig(f'24_{filename_prefix}_{qoi}_scatter_log.png', dpi=600)
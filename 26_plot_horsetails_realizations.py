# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from math import floor, log10
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")

#load results from xlsx file into dictionary of dataframes (one dataframe for each xlsx sheet/qoi)

data_folder='./input_output_datasets'
filename='snl_129I_time.xlsx'

filename_prefix=filename.replace(".xlsx","")

# Import data
qoi='I-129 concentrations'

realization_data = pd.read_excel(os.path.join(data_folder,filename),sheet_name='Sheet2',skiprows=5,header=[0,1], index_col=0).T


realization_data_all=realization_data.reset_index(drop=True)
realization_data_all.index.name='Realization'

#realization_data_melted=realization_data.reset_index().melt(id_vars=['Aleatory','Epistemic'], var_name='timestep',value_name=qoi)

realization_data_all_melted=realization_data_all.reset_index().melt(id_vars=['Realization'], var_name='timestep',value_name=qoi)



#create figure, set dimensions
fig, ax = plt.subplots(1,1,figsize=(8,6))




g_real = sns.lineplot(ax=ax,
    data=realization_data_all_melted,
    x='timestep', y=qoi,  
    units='Realization', 
    dashes=False,
    #palette =palette,
    alpha=0.5, color='0.1',
    estimator=None,
    ci=None,
    linewidth=0.1,
)

g_mean_err= sns.lineplot(ax=ax,
    data=realization_data_all_melted,
    x='timestep', y=qoi,  

    dashes=False,
    #palette =palette,
    alpha=1, color='#750851',

    estimator='mean',
    errorbar=('pi',95),
    linewidth=1,
)

g_mean= sns.lineplot(ax=ax,
    data=realization_data_all_melted,
    x='timestep', y=qoi,  

    dashes=False,
    #palette =palette,
    alpha=1, color='#750851',

    estimator='mean',
    errorbar=None,
    linewidth=2,
)




#g.set(xlim=(-5, 1))
ax.set(ylim=(0.1*10e-22, 1.0*10e-7))
ax.set(yscale='log')
#g.set(xscale='log')
ax.set(xlabel=None)
ax.set(ylabel=f"QoI: {qoi}")
ax.ticklabel_format(axis='x', style='scientific', useMathText=True)

#legend
handles_add = [Line2D([0], [0], color="0.1", lw=0.5), 
               Line2D([0], [0], color="#750851", lw=3),
                mpatches.Rectangle((0, 0), 1, 2,color='#750851',alpha=0.5)]
labels_add = ['separate realizations','mean','95% percentile']
leg_add = ax.legend(handles=handles_add,labels=labels_add, loc="lower right")

fig.tight_layout()



fig.savefig(f'26_{filename_prefix}_{qoi}_horsetails.png', dpi=600)
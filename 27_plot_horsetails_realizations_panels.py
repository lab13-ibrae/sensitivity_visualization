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
filename='snl_129I_time.xlsx'

filename_prefix=filename.replace(".xlsx","")

# Import data
qoi='I-129 concentrations'

realization_data = pd.read_excel(os.path.join(data_folder,filename),sheet_name='Sheet2',skiprows=5,header=[0,1], index_col=0).T

realization_data_melted=realization_data.reset_index().melt(id_vars=['Aleatory','Epistemic'], var_name='timestep',value_name=qoi)




#palette = sns.set_palette(sns.color_palette(['0.9']))
g = sns.relplot(data=realization_data_melted, 
                style='Epistemic', 
                col='Aleatory',
                col_wrap=5,
                dashes=False,
                #palette =palette,
                #col_wrap=5, 
                height=3, aspect=1,
                x='timestep', y=qoi, 
                facet_kws={'sharex': False, 'sharey': True},
                alpha=0.5, color='0.1',
                kind='line',
                ci=None,
                linewidth=0.5
                #palette=palette
                )



for real, axes in g.axes_dict.items():
#for axes in g.axes.flat:
    axes.ticklabel_format(axis='both', style='scientific', useMathText=True)
    sns.lineplot(
          data=realization_data_melted[realization_data_melted.Aleatory==real], 
          x='timestep', y=qoi,
          estimator='mean', 
          #errorbar=("pi", 95),
          color="red", linewidth=0.5, ax=axes, legend=False,
     )




g._legend.remove()
g.despine(top=False, right=False, left=False, bottom=False, offset=None, trim=False)
#g.set(xlim=(-5, 1))
#g.set(ylim=(0.5*10e-11, 1.5*10e-8))
g.set(yscale='log')
#g.set(xscale='log')
g.set(xlabel=None)
g.set(ylabel=f"QoI: {qoi}")
g.fig.set_size_inches(15,15)
g.fig.tight_layout()
g.fig.subplots_adjust(hspace=0.25)


g.savefig(f'27_{filename_prefix}_{qoi}_horsetails_panels.png', dpi=600)
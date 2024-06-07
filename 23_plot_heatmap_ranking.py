# -*- coding: utf-8 -*-
#import required libraries
import os
import pandas as pd
import seaborn as sns
import numpy as np
from pylab import rcParams
from matplotlib import pyplot as plt

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")
sns.set(color_codes=True, font_scale=1.2)
rcParams['xtick.labelsize'] = 'small'

#select qoi
qoi='Peak_TotalI129_M'
#qoi="FractionofSpikeinRepository_1My"
#qoi="FractionalMassFluxfromRepo_1Myr"
#qoi="AqEb_RockEb_1Myr"
#qoi="RockAq_RockEb_1Myr"

#load results from xlsx file into one dataframe
data_folder='./sensitivity_results_datasets'
filename='snl_rankings_paper_orig_order.xlsx'
filename_prefix=filename.replace(".xlsx","")

data = pd.read_excel(os.path.join(data_folder,filename),sheet_name=qoi, index_col=0,header=0)

#create figure, set dimensions
fig,ax=plt.subplots(figsize=(9, 9))
#colormap
custom_cmap = sns.diverging_palette(20, 220, as_cmap=True)

ticks=np.linspace(data.min(skipna=True).min(), data.max(skipna=True).max(), 3)
g=sns.heatmap(data,cmap=custom_cmap,ax=ax,linewidths=1, linecolor='#F1F1F1',cbar_kws={'ticks': ticks})

ax.set_facecolor('#ffffff')
ax.grid(False, 'major')
ax.set_xticklabels(g.get_xticklabels(),rotation=0, horizontalalignment='center')
ax.collections[0].colorbar.set_ticklabels(['maximal','medium','minimal',])
ax.collections[0].colorbar.ax.invert_yaxis()
ax.set(ylabel='')


plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)


plt.savefig(f'23_{filename_prefix}_{qoi}_ranking_heatmap.png',dpi=600)
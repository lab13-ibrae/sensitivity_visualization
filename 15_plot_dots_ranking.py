# -*- coding: utf-8 -*-
#import required libraries
import os
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
from pylab import rcParams
from matplotlib.colors import ListedColormap

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
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


##properties of dot replacement
dot_symbol='●'
max_dots=4

#transform data into dots
data_dots=data.astype('Int64')
data_dots=data_dots.applymap(lambda x: dot_symbol*(max_dots+1-x))

#create figure, set dimensions
fig,ax=plt.subplots(figsize=(9, 6))
#annotations work correctly with matplotlib==3.7.3, there is some kind of bug in later versions
g=sns.heatmap(data,
              annot=False,
              cmap=ListedColormap(['white']),
              ax=ax,linewidths=1, 
              linecolor='#F1F1F1',
              cbar=False,
              )

#place dots
g_annot=sns.heatmap(data,
                    annot=data_dots,
                    annot_kws={'va':'center'},
                    cmap=ListedColormap(['white']),
                    ax=ax,linewidths=1, 
                    linecolor='#F1F1F1',
                    fmt="",
                    cbar=False)

ax.set_facecolor('#ffffff')
ax.grid(False, 'major')
ax.set_xticklabels(g.get_xticklabels(),rotation=0, horizontalalignment='center')
ax.xaxis.tick_top()
ax.set(ylabel='')
ax.tick_params(left=False, bottom=False,top=False)


plt.subplots_adjust(left=0.15, right=0.99, bottom=0.01, top=0.88)

plt.savefig(f'16_{filename_prefix}_{qoi}_ranking_dots.png',dpi=600)
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

filename='snl_rankings_sorted.xlsx'
filename_prefix=filename.replace(".xlsx","")

data = pd.read_excel(os.path.join(data_folder,filename),sheet_name=qoi, index_col=None,header=0)


#data_sorted=
#reshape data
data_melted=data.melt(id_vars=['parameter'],value_vars=list(data.columns),var_name='method',value_name='ranking')

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")
#create figure, set dimensions
fig,ax=plt.subplots(figsize=(9, 6))



colors=[
    #Sobol'
    '#D55E00',
    #Spearman
    '#0072B2',
    #PAWN
    '#009E73',
    #Gini/SHAP
    '#CC79A7',
    ]

palette = sns.set_palette(sns.color_palette(colors))
g=sns.lineplot(ax=ax, data=data_melted , x="parameter", y="ranking",hue='method',
               style="method",markers={"Sobol'":"P", 'Spearman':"d", 'PAWN':"X", 'Gini/SHAP':"8"}, markersize=10, dashes=False, palette =palette)

ax.set_facecolor('#ffffff')
ax.grid(False, 'major')
#ax.set_xticklabels(g.get_xticklabels(),rotation=0, horizontalalignment='center')
ax.xaxis.tick_bottom()
ax.set(ylabel='Ranking')
ax.set(xlabel='Parameter')
ax.tick_params(left=False, bottom=False,top=False)
ax.invert_yaxis()
fig.tight_layout()
#plt.subplots_adjust(left=0.15, right=0.99, bottom=0.01, top=0.88)

plt.savefig(f'21_{filename_prefix}_{qoi}_ranking_lines.png',dpi=600)
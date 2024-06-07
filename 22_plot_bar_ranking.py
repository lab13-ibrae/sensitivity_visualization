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

max_ranking=data_melted['ranking'].max()
min_ranking=data_melted['ranking'].min()

data_melted['ranking_reverse']=max_ranking+min_ranking-data_melted['ranking']
data_melted['ranking_reverse']=data_melted['ranking_reverse'].fillna(value=-1)

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")
#create figure, set dimensions
fig,ax=plt.subplots(figsize=(6, 6))


#palette
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
g=sns.barplot(ax=ax, data=data_melted , y="parameter", x="ranking_reverse",hue='method',
              palette =palette)

ax.set_facecolor('#ffffff')
ax.grid(False, 'major')
#ax.set_xticklabels(g.get_xticklabels(),rotation=0, horizontalalignment='center')
ax.xaxis.tick_bottom()


labels = [item.get_text() for item in ax.get_xticklabels()]
labels.reverse()
labels[0]=''
ax.set_xticklabels(labels)


ax.set(ylabel='Parameter')
ax.set(xlabel='Ranking')
ax.tick_params(left=False, bottom=False,top=False)
#ax.invert_yaxis()
fig.tight_layout()
#plt.subplots_adjust(left=0.15, right=0.99, bottom=0.01, top=0.88)

plt.savefig(f'22_{filename_prefix}_{qoi}_ranking_bar.png',dpi=600)
# -*- coding: utf-8 -*-
#import required libraries
import os
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")

#load results from xlsx file into one dataframe
data_folder='./sensitivity_results_datasets'

filename='snl_129I_time_no_graph_gini_bootstrap.xlsx'
filename_prefix=filename.replace(".xlsx","")

sens_data=pd.read_excel(os.path.join(data_folder,filename),sheet_name='Gini',index_col=0)

#reshape data
sens_data_melted=sens_data.melt(id_vars=['timestep','N_trial'],var_name='parameter',value_name='importance')

sens_data_melted_mean=sens_data_melted.groupby(['timestep', 'parameter'],as_index=False)['importance'].mean()
#set custom palette
##~Okabe&Ito palette
palette= {
          'pBuffer':'#F0E442','meanWPrate':'#E69F00','stdWPrate':'#D55E00',
                      'IRF':'#0072B2','rateUNF':'#009E73','kGlacial':'#56B4E9',
                      'permDRZ':'#CC79A7','permBuffer':'#000000',
                      }



g = sns.relplot(data=sens_data_melted,
    x='timestep', y="importance", col="parameter", hue="parameter",palette=palette,
    errorbar=("pi", 95),
    #errorbar="sd",
    kind="line",  linewidth=1.5, zorder=5,
    col_wrap=3, height=2.5, aspect=1.5, legend=False, facet_kws={'sharey': False, 'sharex': False}
)




for par, ax in g.axes_dict.items():
    sns.lineplot(
          data=sens_data_melted_mean, x="timestep", y="importance", units="parameter",
          estimator=None, color=".7", linewidth=0.5, ax=ax, legend=False,
     )
    #Add the title as an annotation within the plot
    ax.text(.98, .9, par,ha='right', transform=ax.transAxes, fontweight="bold", fontsize=12)
    ax.set_ylim(0,1)
    ax.set_yticks(np.linspace(0,1,11))

    ax.spines["top"].set_visible(True)
    ax.spines["bottom"].set_visible(True)
    ax.spines["right"].set_visible(True)
    ax.spines["left"].set_visible(True)
    ax.tick_params(axis='both',length=1, pad=1,which='major', labelsize=8)
    ax.grid(color='lightgrey', linestyle=':', linewidth=0.7)
    #ax.set_xticks(ax.get_xticks()[::2],fontsize=10)
    ax.set_xticks(ax.get_xticks()[::2])
g.set(xscale = 'log')
g.set_titles("")
g.set_axis_labels("Time, years", r"Sensitivity indices")
g.tight_layout()

#plot title
g.fig.suptitle(f"Gini importance measure.\nStatistics via bootstrap over 50 train/test splits.\nQoI: I-129 concentrations", x=0.84,y=0.16, fontweight="bold",fontsize=12)

#legend
handles_add = [Line2D([0], [0], color=".5", lw=1.2),
                mpatches.Rectangle((0, 0), 1, 2,color='0.5',alpha=0.5)]
labels_add = ['mean importance','95% percentile']
leg_add = ax.legend(handles=handles_add,labels=labels_add, loc="lower right",bbox_to_anchor=[1.9,0.7])
g.fig.add_artist(leg_add)

g.savefig(f"17_{filename_prefix}_panels_with_err.png", dpi=600)
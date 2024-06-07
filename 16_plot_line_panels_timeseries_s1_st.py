# -*- coding: utf-8 -*-
#import required libraries
import os
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")

#load results from xlsx file into one dataframe
data_folder='./sensitivity_results_datasets'
filename='snl_129I_time_no_graph_s1_st_s2_dakota.xlsx'
#filename='snl_129I_time_no_graph_s1_st_chaospy.xlsx'
filename_prefix=filename.replace(".xlsx","")

sens_data=pd.read_excel(os.path.join(data_folder,filename),sheet_name='S1_ST',index_col=None)

#reshape data
sens_data_melted=sens_data.melt(id_vars=['timestep','parameter'],var_name='sens_ind',value_name='value')

#set custom palette
##~Okabe&Ito palette
palette= {
          'pBuffer':'#F0E442','meanWPrate':'#E69F00','stdWPrate':'#D55E00',
                      'IRF':'#0072B2','rateUNF':'#009E73','kGlacial':'#56B4E9',
                      'permDRZ':'#CC79A7','permBuffer':'#000000',
                      }


line_dashes=[(6, 3),(1, 0)]
g = sns.relplot(data=sens_data_melted[sens_data_melted.sens_ind.isin(['S1','ST'])],
    x='timestep', y="value", col="parameter", hue="parameter",style="sens_ind",palette=palette,dashes=line_dashes,
    kind="line",  linewidth=1.5, zorder=5,
    col_wrap=3, height=2.5, aspect=1.5, legend=False, facet_kws={'sharey': False, 'sharex': False}
)


for par, ax in g.axes_dict.items():
    sns.lineplot(
          data=sens_data_melted[sens_data_melted.sens_ind=='ST'], x="timestep", y="value", units="parameter",
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

handles = [Line2D([0], [0], color=".5", lw=1.2, dashes=list(line_dashes[0])),
                Line2D([0], [0], color=".5", lw=1.2,dashes=list(line_dashes[1])),]

labels = ['Main','Total']

g.fig.legend(handles=handles, handlelength=1.7,labelspacing=0.05, labels=labels, loc='upper left', ncol=1, 
             title_fontsize=9,fontsize=10,bbox_to_anchor=(0.07, 0.965))

#plot title
g.fig.suptitle(f"Main and total Sobol' indices.\nQoI: I-129 concentrations", x=0.85,y=0.22, fontweight="bold",fontsize=12)
g.fig.subplots_adjust(top=0.96, bottom=0.07)



g.savefig(f"16_{filename_prefix}_panels.png", dpi=600)
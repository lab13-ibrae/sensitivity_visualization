# -*- coding: utf-8 -*-
#import required libraries
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")

#load results from xlsx file into one dataframe
data_folder='./sensitivity_results_datasets'
filename='snl_129I_time_no_graph_s1_st_s2_dakota.xlsx'
#filename='snl_129I_time_no_graph_s1_st_chaospy.xlsx'
filename_prefix=filename.replace(".xlsx","")

sens_data=pd.read_excel(os.path.join(data_folder,filename),sheet_name='S1_ST',index_col=None)

#set custom palette

##~Okabe&Ito palette
palette= {
          'pBuffer':'#F0E442','meanWPrate':'#E69F00','stdWPrate':'#D55E00',
                      'IRF':'#0072B2','rateUNF':'#009E73','kGlacial':'#56B4E9',
                      'permDRZ':'#CC79A7','permBuffer':'#000000',
                      }

#create figure, set dimensions
fig, ax = plt.subplots(1,1,figsize=(8,6))

g = sns.lineplot(ax=ax,
    data=sens_data,
    x='timestep', y="ST",  hue="parameter",palette=palette,
      linewidth=2.0, zorder=5,
     legend=True,
)



g.set(xscale = 'log')
#g.set_titles("")
ax.set_ylabel(r"$S_T$")
ax.set_xlabel(r"Time, years")
ax.set_ylim(0,1.2)
ax.tick_params(axis='x', which='major', labelsize=10)
# get the legend object
leg = ax.legend()
handles, labels = ax.get_legend_handles_labels()
# change the line width for the legend
for line in leg.get_lines():
    line.set_linewidth(4.0)
leg.set_title("Parameters")
#order of legend items
plt.legend(handles[::-1], labels[::-1],loc='upper right')
#plot title
plt.title(f"Sobol' total sensitivity indices", y=1, fontweight="bold",fontsize=13)
fig.tight_layout()



fig.savefig(fname=f"11_{filename_prefix}_line_st.png", dpi=600)
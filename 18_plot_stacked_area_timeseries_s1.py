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

#reshape dataframe
df_st=sens_data[['timestep','parameter','ST']].set_index('parameter')
df_s1=sens_data[['timestep','parameter','S1']].set_index('parameter')
par_names=list(list(sens_data.parameter.unique()))
df_unstacked=df_s1.reset_index().pivot(columns='parameter', index='timestep', values='S1')
df_unstacked=df_unstacked[par_names]

#set custom palette
##~Okabe&Ito palette
palette= {
          'pBuffer':'#F0E442','meanWPrate':'#E69F00','stdWPrate':'#D55E00',
                      'IRF':'#0072B2','rateUNF':'#009E73','kGlacial':'#56B4E9',
                      'permDRZ':'#CC79A7','permBuffer':'#000000',
                      }

#create figure, set dimensions
fig, ax = plt.subplots(1,1,figsize=(8,6))

ax.hlines(y = 1, xmin = 1000, xmax = 1000000, color = '#343837', linestyles='dashed',linewidth = 2, label='whole variance')

df_unstacked.plot(ax=ax,kind='area', stacked=True, color=palette,alpha=0.8,linewidth=0)
    
ax.set_xscale('log')
#g.set_titles("")
ax.set_ylabel(r"$S_1$")
ax.set_xlabel(r"Time, years")
ax.set_ylim(0,1.1)
ax.tick_params(axis='x', which='major', labelsize=10)

# get the legend object
leg = ax.legend()
# change the line width for the legend
for line in leg.get_lines():
    line.set_linewidth(4.0)
 
#reverse order
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1],loc='upper left',title='Parameters')
#plot title
plt.title(f"Main Sobol' indices. QoI: I-129 concentrations", y=1, fontweight="bold",fontsize=13)
fig.tight_layout()

fig.savefig(fname=f"18_{filename_prefix}_stacked_area.png", dpi=600)
# -*- coding: utf-8 -*-
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import floor, log10


#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")


#load results from xlsx file into one dataframe
data_folder='./sensitivity_results_datasets'
filename='snl_129I_time_no_graph_s1_st_s2_dakota.xlsx'
#filename='snl_129I_time_no_graph_s1_st_chaospy.xlsx'
filename_prefix=filename.replace(".xlsx","")

sens_data=pd.read_excel(os.path.join(data_folder,filename),sheet_name='S1_ST',index_col=None)

#reshape data
df_st=sens_data[['timestep','parameter','ST']].set_index('parameter')
df_s1=sens_data[['timestep','parameter','S1']].set_index('parameter')
par_names=list(list(sens_data.parameter.unique()))
df_unstacked=df_st.reset_index().pivot_table(columns='timestep', index='parameter', values='ST',sort=False)

#transform exponential numbers into powers of 10
def sci_notation(num, decimal_digits=0, precision=None, exponent=None):

    if exponent is None:
        exponent = int(floor(log10(abs(num))))
    coeff = round(num / float(10**exponent), decimal_digits)
    if precision is None:
        precision = decimal_digits
    if coeff!=1:
        return "${0:.{2}f}\cdot10^{{{1:d}}}$".format(coeff, exponent, precision)
    else:
        return "$10^{{{1:d}}}$".format(coeff, exponent, precision)


#colormap
custom_cmap = sns.diverging_palette(220, 20, as_cmap=True)

#create figure, set dimensions
fig, ax = plt.subplots(1,1,figsize=(8,6))

g = sns.heatmap(df_unstacked,cmap=custom_cmap, vmin=0, 
                cbar_kws={'location':"right","shrink": 0.5,"orientation": "vertical",}
                )

#adjust ticks
every_pos=4
tick_pos = np.arange(len(df_unstacked.columns))[::every_pos]
tick_labels = [sci_notation(df_unstacked.columns.values[x]) for x in tick_pos]
ax.set_xticks(tick_pos)
ax.set_xticklabels(tick_labels, rotation=0)

ax.set_xlabel('Time, years')
ax.set_ylabel('Parameters')

ax.spines[:].set_visible(False)

ax.hlines(np.arange(df_unstacked.shape[0]), *ax.get_xlim(),colors='0.9',linewidth=3.0)
#ax.vlines(tick_pos, *ax.get_xlim(),colors='0.9',linewidth=2.)

cbar = ax.collections[0].colorbar
cbar.set_label(r'$S_T$ index',fontsize=12,labelpad=20, y=1.1,x=-0.9, ha='right', rotation=0)

plt.title(f"Total Sobol' indices. QoI: I-129 concentrations", y=1, fontweight="bold",fontsize=13)

fig.tight_layout()

fig.savefig(fname=f"14_{filename_prefix}_heatmap.png", dpi=600)
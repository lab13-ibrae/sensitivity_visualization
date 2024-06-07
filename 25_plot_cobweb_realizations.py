# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import paxplot
from math import floor, log10
import numpy as np
#set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
sns.set_theme(style="whitegrid")

#load results from xlsx file into dictionary of dataframes (one dataframe for each xlsx sheet/qoi)
#data_folder='./sensitivity_results_datasets'
data_folder='./input_output_datasets'
filename='snl_qoi_realizations.xlsx'

filename_prefix=filename.replace(".xlsx","")

# Import data

realization_data = pd.read_excel(os.path.join(data_folder,filename),sheet_name='all')
parameters=list(realization_data.columns[1:9])
qois=list(realization_data.columns[9:])

    
#select qoi
qoi='Peak_TotalI129_M'
#qoi="FractionofSpikeinRepository_1Myr"
#qoi="FractionalMassFluxfromRepo_1Myr"
#qoi="AqEb_RockEb_1Myr"
#qoi="RockAq_RockEb_1Myr"


all_realizations_data_qoi=realization_data[['Realization']+parameters+[qoi]]

##parallel axes plot are rendered with the help of paxplot library: https://github.com/kravitsjacob/paxplot

#for realization in range(1,26,1):
for realization in [1,3,8,25]:
#realization=1
    selected_realization_data_qoi=all_realizations_data_qoi[all_realizations_data_qoi.Realization==realization].loc[:, all_realizations_data_qoi.columns != 'Realization']
    
    other_realizations_data_qoi=all_realizations_data_qoi[all_realizations_data_qoi.Realization!=realization].loc[:, all_realizations_data_qoi.columns != 'Realization']
    
    #set plot style: https://www.python-graph-gallery.com/104-seaborn-themes
    #sns.set_theme(style="whitegrid")
    #create figure, set dimensions
    #fig,ax=plt.subplots(figsize=(6, 6))
    
    
    
    # Split data
    df_highlight = selected_realization_data_qoi
    cols = df_highlight.columns
    df_grey = other_realizations_data_qoi
    
    # Create figure
    paxfig = paxplot.pax_parallel(n_axes=len(cols))
    paxfig.plot(df_highlight.to_numpy(),
                line_kwargs={'linewidth':0.5}
                )
    
    # Add colorbar for highlighted
    color_col = 8
    paxfig.add_colorbar(
        ax_idx=color_col,
        cmap='viridis',
        colorbar_kwargs={'label': cols[color_col], }
    )
    
    #move colorbar
    colorbar_ax=plt.gcf().axes[-1]
    colorbar_pos = colorbar_ax.get_position()
    colorbar_pos.x0=colorbar_pos.x0+0.03
    colorbar_pos.x1=colorbar_pos.x1+0.03
    colorbar_ax.set_position(colorbar_pos)
    
    
    # Add grey data
    paxfig.plot(
        df_grey.to_numpy(),
        line_kwargs={'alpha': 0.2, 'color': '0.3', 'zorder': 0, 'linewidth':0.5}
    )
    
    # Add labels
    paxfig.set_labels(cols)
    
    #color of axes
    for ax in plt.gcf().axes[:-1]:
        ax.spines['left'].set_color('0.4')
        ax.spines['top'].set_color('0.4')
        ax.spines['bottom'].set_color('0.4')
        
    #nice ticks
    def sci_notation(num, decimal_digits=0, precision=None, exponent=None):
        if num==0:
            return f"${num}$"
        else:
            if exponent is None:
                exponent = int(floor(log10(abs(num))))
            if abs(exponent)<3:
                return f"{round(num,2)}"
            else:
                coeff = round(num / float(10**exponent), decimal_digits)
                if precision is None:
                    precision = decimal_digits
                if coeff!=1:
                    return "${0:.{2}f}\cdot10^{{{1:d}}}$".format(coeff, exponent, precision)
                else:
                    return "$10^{{{1:d}}}$".format(coeff, exponent, precision)
    
    num_ticks=5
    for col_n,col in enumerate(cols):
        col_min=all_realizations_data_qoi[col].min()
        col_max=all_realizations_data_qoi[col].max()
        ticks = list(np.linspace(col_min, col_max, num_ticks))
        labels=[sci_notation(t) for t in ticks]
        paxfig.set_ticks(
            ax_idx=col_n,
            ticks=ticks,
            labels=labels
        )
    
    
    #title
    plt.suptitle(f"Stochastic realizations for QoI:{qoi}.\nAleatory realization #{realization} highlighted", y=0.975);
    
    
    #figure size
    plt.gcf().set_size_inches(14,6)
    
    
    plt.show()
    
    
    plt.savefig(f'25_{filename_prefix}_{qoi}_real_{realization}_cobweb.png', dpi=600)
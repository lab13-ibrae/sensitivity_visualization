# -*- coding: utf-8 -*-
#import required libraries
import os
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pylab import rcParams

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

data = pd.read_excel(os.path.join(data_folder,filename),sheet_name=qoi, index_col=None,header=0)

#reshape data
data_melted=data.melt(id_vars=['parameter'],value_vars=list(data.columns),var_name='metric',value_name='ranking')
max_ranking=data_melted['ranking'].max()
min_ranking=data_melted['ranking'].min()

data_melted['ranking_reverse']=max_ranking+min_ranking-data_melted['ranking']
data_melted['ranking_reverse']=data_melted['ranking_reverse'].fillna(value=-1)



# adapted from https://github.com/drazenz/heatmaps/blob/master/heatmap/heatmap.py
def heatmap(x, y, **kwargs):
    if 'color' in kwargs:
        color = kwargs['color']
    else:
        color = [1]*len(x)
    if 'palette' in kwargs:
        palette = kwargs['palette']
        n_colors = len(palette)
    else:
        n_colors = 256 # Use 256 colors for the diverging color palette
        palette = sns.color_palette("Blues", n_colors) 

    if 'color_range' in kwargs:
        color_min, color_max = kwargs['color_range']
    else:
        color_min, color_max = min(color), max(color) # Range of values that will be mapped to the palette, i.e. min and max possible correlation
    def value_to_color(val):
        if color_min == color_max:
            return palette[-1]
        else:
            val_position = float((val - color_min)) / (color_max - color_min) # position of value in the input range, relative to the length of the input range
            val_position = min(max(val_position, 0), 1) # bound the position betwen 0 and 1
            ind = int(val_position * (n_colors - 1)) # target index in the color palette
            return palette[ind]
    if 'size' in kwargs:
        size = kwargs['size']
    else:
        size = [1]*len(x)

    if 'size_range' in kwargs:
        size_min, size_max = kwargs['size_range'][0], kwargs['size_range'][1]
    else:
        size_min, size_max = min(size), max(size)

    size_scale = kwargs.get('size_scale', 500)

    def value_to_size(val):
        if size_min == size_max:
            return 1 * size_scale
        else:
            val_position = (val - size_min) * 0.99 / (size_max - size_min) + 0.01 # position of value in the input range, relative to the length of the input range
            val_position = min(max(val_position, 0), 1) # bound the position betwen 0 and 1
            return val_position * size_scale
    if 'x_order' in kwargs: 
        x_names = [t for t in kwargs['x_order']]
    else:
        x_names = [t for t in sorted(set([v for v in x]))]
    x_to_num = {p[1]:p[0] for p in enumerate(x_names)}

    if 'y_order' in kwargs: 
        y_names = [t for t in kwargs['y_order']]
    else:
        y_names = [t for t in sorted(set([v for v in y]))]
    y_to_num = {p[1]:p[0] for p in enumerate(y_names)}

    plot_grid = plt.GridSpec(1, 15, hspace=0.2, wspace=0.1) # Setup a 1x10 grid
    ax = plt.subplot(plot_grid[:,:-1]) # Use the left 14/15ths of the grid for the main plot

    marker = kwargs.get('marker', 's')

    kwargs_pass_on = {k:v for k,v in kwargs.items() if k not in [
         'color', 'palette', 'color_range', 'size', 'size_range', 'size_scale', 'marker', 'x_order', 'y_order', 'xlabel', 'ylabel'
    ]}

    ax.scatter(
        x=[x_to_num[v] for v in x],
        y=[y_to_num[v] for v in y],
        marker=marker,
        s=[value_to_size(v) for v in size], 

        c=[value_to_color(v) for v in color],
        **kwargs_pass_on
    )
    ax.set_xticks([v for k,v in x_to_num.items()])
    #ax.set_xticklabels([k for k in x_to_num], rotation=45, horizontalalignment='right')
    ax.set_xticklabels([k for k in x_to_num], rotation=0, horizontalalignment='center')
    ax.set_yticks([v for k,v in y_to_num.items()])
    ax.set_yticklabels([k for k in y_to_num])

    ax.grid(False, 'major')
    ax.grid(True, 'minor',color='#F1F1F1')
    
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)

    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    #ax.set_facecolor('#F1F1F1')
    ax.set_facecolor('#ffffff')

    ax.set_xlabel(kwargs.get('xlabel', ''))
    ax.set_ylabel(kwargs.get('ylabel', ''))

    # Add color legend on the right side of the plot
    if color_min < color_max:
        ax = plt.subplot(plot_grid[:,-1]) # Use the rightmost column of the plot

        col_x = [0]*len(palette) # Fixed x coordinate for the bars
        bar_y=np.linspace(color_min, color_max, n_colors) # y coordinates for each of the n_colors bars

        bar_height = bar_y[1] - bar_y[0]
        ax.barh(
            y=bar_y,
            width=[5]*len(palette), # Make bars 5 units wide
            left=col_x, # Make bars start at 0
            height=bar_height,
            color=palette,
            linewidth=0
        )
        ax.set_xlim(1, 2) # Bars are going from 0 to 5, so lets crop the plot somewhere in the middle
        ax.grid(False) # Hide grid
        ax.set_facecolor('white') # Make background white
        ax.set_xticks([]) # Remove horizontal ticks
        ax.set_yticks(np.linspace(min(bar_y), max(bar_y), 3)) # Show vertical ticks for min, middle and max
        ax.set_yticklabels(['minimal','medium','maximal']) # Show vertical ticks for min, middle and max
        ax.yaxis.tick_right() # Show vertical ticks on the right 


#create figure, set dimensions
fig=plt.figure(figsize=(9, 9))

heatmap(
    x=data_melted['metric'], # Column to use as horizontal dimension
    y=data_melted['parameter'], # Column to use as vertical dimension
    size_range=[0,10],
    color_range=[min_ranking, max_ranking],
    size_scale=2500, # Change this to see how it affects the plot
    size=data_melted['ranking_reverse'], # Values to map to size, here we use number of items in each bucket

    x_order=list(data.columns)[1:], # Sort order for x labels
    y_order=list(data['parameter'])[::-1], # Sort order for y labels
    color=data_melted['ranking_reverse'], # Values to map to color, here we use number of items in each bucket
    #palette=sns.cubehelix_palette(128)[::-1], # We'll use black->red palette
    #palette=sns.color_palette("viridis")[::-1]
    palette=sns.color_palette("Greys")
)


plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)

plt.savefig(f'23_{filename_prefix}_{qoi}_ranking_heatmap_size_gray.png',dpi=600)
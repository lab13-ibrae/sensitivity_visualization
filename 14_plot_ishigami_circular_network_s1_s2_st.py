# -*- coding: utf-8 -*-
import os
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import matplotlib.collections as mcoll
from matplotlib.colors import LinearSegmentedColormap
import colorsys
import matplotlib.colors as mpl_colors


#load demo data
data_folder='./sensitivity_results_datasets'
filename='si_ishigami_demo.pkl'
with open(os.path.join(data_folder,filename), 'rb') as handle:
    si_tmp = pickle.load(handle)
    
problem=si_tmp['problem']

def S2_to_dict(matrix, problem):
    result = {}
    names = list(problem["names"])
    
    for i in range(problem["num_vars"]):
        for j in range(i+1, problem["num_vars"]):
            if names[i] not in result:
                result[names[i]] = {}
            if names[j] not in result:
                result[names[j]] = {}
                
            result[names[i]][names[j]] = result[names[j]][names[i]] = float(matrix[i][j])
            
    return result


#transform
si_for_plot = {} #create dictionary to store new
si_for_plot['S1']={k : float(v) for k, v in zip(problem["names"], si_tmp["S1"])}
#si_for_plot['S1_conf']={k : float(v) for k, v in zip(problem["names"], si_tmp["S1_conf"])}
si_for_plot['S2'] = S2_to_dict(si_tmp['S2'], problem)
#si_for_plot['S2_conf'] = S2_to_dict(si_tmp['S2_conf'], problem)
si_for_plot['ST']={k : float(v) for k, v in zip(problem["names"], si_tmp["ST"])}
#si_for_plot['ST_conf']={k : float(v) for k, v in zip(problem["names"], si_tmp["ST_conf"])}


####plotting
## radial convergence graphs (aka chord graphs) for Sobol Sensitivity Analysis results in a dictionary format. 
## source modified from https://github.com/antonia-had) and (https://github.com/ubi15/).

# Get list of parameters
parameters = list(si_for_plot['S1'].keys())
# Set min index value, for the effects to be considered significant
index_significance_value = 0.005


#layout settings.
node_size_min = 10 # Max and min node size
node_size_max = 25
border_size_min = 1 # Max and min node border thickness
border_size_max = 6
edge_width_min = 1 # Max and min edge thickness
edge_width_max = 10
edge_distance_min = 0.1 # Max and min distance of the edge from the center of the circle
edge_distance_max = 0.6 # Only applicable to the curved edges


# Define circle center and radius
center = [0.0,0.0] 
radius = 1.0

# Function to get distance between two points
def distance(p1,p2):
    return np.sqrt(((p1-p2)**2).sum())

# Function to get middle point between two points
def middle(p1,p2):
    return (p1+p2)/2

# Function to get the vertex of a curve between two points
def vertex(p1,p2,c):
    m = middle(p1,p2)
    curve_direction = c-m
    return m+curve_direction*(edge_distance_min+edge_distance_max*(1-distance(m,c)/distance(c,p1)))

# Function to get the angle of the node from the center of the circle
def angle(p,c):
    # Get x and y distance of point from center
    [dx,dy] = p-c 
    if dx == 0: # If point on vertical axis (same x as center)
        if dy>0: # If point is on positive vertical axis
            return np.pi/2.
        else: # If point is on negative vertical axis
            return np.pi*3./2.
    elif dx>0: # If point in the right quadrants
        if dy>=0: # If point in the top right quadrant
            return np.arctan(dy/dx)
        else: # If point in the bottom right quadrant
            return 2*np.pi+np.arctan(dy/dx)
    elif dx<0: # If point in the left quadrants
        return np.pi+np.arctan(dy/dx)

# set up graph with all parameters as nodes and draw all second order (S2) indices as edges in the network. 
#For every S2 index, we need a Source parameter,a Target parameter, and the Weight of the line, given by the S2 index itself. 


combs = [list(c) for c in list(itertools.combinations(parameters, 2))]

Sources = list(list(zip(*combs))[0])
Targets = list(list(zip(*combs))[1])
# Sometimes computing errors produce negative Sobol indices. The following reads
# in all the indices and also ensures they are between 0 and 1.
Weights = [max(min(x, 1), 0) for x in [si_for_plot['S2'][Sources[i]][Targets[i]] for i in range(len(Sources))]]
Weights = [index_significance_value if x<index_significance_value else x for x in Weights]

# Set up graph
G = nx.Graph()
# Draw edges with appropriate weight
for s,t,weight in zip(Sources, Targets, Weights):
    G.add_edges_from([(s,t)], w=weight)

# Generate dictionary of node postions in a circular layout
Pos = nx.circular_layout(G)

#Normalize node size according to first order (S1) index. 
#Read in S1 indices,ensure they're between 0 and 1 and normalize them within the max and min range of node sizes.
#Then, normalize edge thickness according to S2. 


# Node size
first_order = [max(min(x, 1), 0) for x in [si_for_plot['S1'][key] for key in si_for_plot['S1']]]
first_order = [0 if x<index_significance_value else x for x in first_order]
node_size = [node_size_min*(1 + (node_size_max-node_size_min)*k/max(first_order)) for k in first_order]
# Node border thickness
total_order = [max(min(x, 1), 0) for x in [si_for_plot['ST'][key] for key in si_for_plot['ST']]]
total_order = [0 if x<index_significance_value else x for x in total_order]
border_size = [border_size_min*(1 + (border_size_max-border_size_min)*k/max(total_order)) for k in total_order]
# Edge thickness
edge_width = [edge_width_min*((edge_width_max-edge_width_min)*k/max(Weights)) for k in Weights]

# # Plot nodes with straight lines
# nx.draw_networkx_nodes(G, Pos, node_size=node_size, node_color='#98B5E2', 
#                        edgecolors='#1A3F7A', linewidths = border_size)
# nx.draw_networkx_edges(G, Pos, width=edge_width, edge_color='#2E5591', alpha=0.7)
# names = nx.draw_networkx_labels(G, Pos, font_size=12, font_color='#0B2D61', font_family='sans-serif')
# for node, text in names.items():
#     position = (radius*1.1*np.cos(angle(Pos[node],center)), radius*1.1*np.sin(angle(Pos[node],center)))
#     text.set_position(position)
#     text.set_clip_on(False)
# plt.gcf().set_size_inches(9,9) # Make figure a square
# plt.axis('off')

# Calculate all distances between 1 node and all the others (all distances are the same since they're in a circle).
#We'll need this to identify the curves we'll be drawing along the perimeter (i.e. those that are next to each other).

min_distance = round(min([distance(Pos[list(G.nodes())[0]],Pos[n]) for n in list(G.nodes())[1:]]), 1)

# Figure to generate the curved edges between two points
def xy_edge(p1,p2): # Point 1, Point 2
    m = middle(p1,p2) # Get middle point between the two nodes
    # If the middle of the two points falls very close to the center, then the line between the two points is simply straight
    if distance(m,center)<1e-6:
        xpr = np.linspace(p1[0],p2[0],10)
        ypr = np.linspace(p1[1],p2[1],10)
    # If the distance between the two points is the minimum (i.e. they are next to each other), draw the edge along the perimeter
    elif distance(p1,p2)<=min_distance:
        # Get angles of two points
        p1_angle = angle(p1,center)
        p2_angle = angle(p2,center)
        # Check if the points are more than a hemisphere apart
        if max(p1_angle,p2_angle)-min(p1_angle,p2_angle) > np.pi:
            radi = np.linspace(max(p1_angle,p2_angle)-2*np.pi,min(p1_angle,p2_angle))
        else:
            radi = np.linspace(min(p1_angle,p2_angle),max(p1_angle,p2_angle))
        xpr = radius*np.cos(radi)+center[0]
        ypr = radius*np.sin(radi)+center[1]  
    # Otherwise, draw curve (parabola)
    else: 
        edge_vertex = vertex(p1,p2,center)
        a = distance(edge_vertex, m)/((distance(p1,p2)/2)**2)
        yp = np.linspace(-distance(p1,p2)/2, distance(p1,p2)/2,100)
        xp = a*(yp**2)
        xp += distance(center,edge_vertex)
        theta_m = angle(middle(p1,p2),center)
        xpr = np.cos(theta_m)*xp - np.sin(theta_m)*yp
        ypr = np.sin(theta_m)*xp + np.cos(theta_m)*yp
        xpr += center[0]
        ypr += center[1]
    return xpr,ypr



#define palette
# palette=sns.mpl_palette('viridis', n_colors=len(parameters))
# pal_dict={}
# for i,par in enumerate(parameters):
#     pal_dict[par]=palette[i]
#sns.palplot(palette)
#custom palette dictionary
# pal_dict_hex={
# 'x1':'#035265',
# 'x2':'#C79A03',
# 'x3':'#BF1755',
#     }

pal_dict_hex={
 'x1':'#0072B2',
 'x2':'#19675D',
 'x3':'#CC79A7',
     }


pal_dict = {k: mpl_colors.hex2color(v) for k, v in pal_dict_hex.items()}

###gradient lines
def colorline(
    x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0),
        linewidth=3, alpha=1.0):
    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])
    z = np.asarray(z)
    segments = make_segments(x, y)
    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)
    ax = plt.gca()
    ax.add_collection(lc)
    return lc

def make_segments(x, y):
    #Create list of line segments from x and y coordinates, in the correct format  for LineCollection:
    #an array of the form numlines x (points per line) x 2 (x and y) array
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments


def scale_light_and_sat(rgb, scale_l,scale_s):
    # convert rgb to hls
    h, l, s = colorsys.rgb_to_hls(*rgb)
    # manipulate h, l, s values and return as rgb
    return colorsys.hls_to_rgb(h, min(1, l * scale_l), min(1, s * scale_s))



#Draw network. This will draw the graph with curved lines along the edges and across the circle. 
fig = plt.figure(figsize=(8,9))
ax = fig.add_subplot(1,1,1)
for i, e in enumerate(G.edges()):
    x,y=xy_edge(Pos[e[0]],Pos[e[1]])
    #ax.plot(x,y,'-', c='#2E5591',lw=edge_width[i],alpha=0.7)
    #2 colors are pal_dict[e[0]] and pal_dict[e[1]]
    #colorline(x, y, cmap=plt.get_cmap('viridis'), linewidth=edge_width[i],alpha=0.7)
    par_name_for_color1=e[0].replace("(-)",'').replace(" ",'')
    par_name_for_color2=e[1].replace("(-)",'').replace(" ",'')
    colorline(x, y, 
              #cmap=LinearSegmentedColormap.from_list("node_colors",[pal_dict[e[0]],pal_dict[e[1]]] ),
              cmap=LinearSegmentedColormap.from_list("node_colors",[pal_dict[par_name_for_color2],pal_dict[par_name_for_color1]] ),
              linewidth=edge_width[i],alpha=0.7)
for i, n in enumerate(G.nodes()):
    par_name_for_color=n.replace("(-)",'').replace(" ",'')
    ax.plot(Pos[n][0],Pos[n][1], 'o', 
            #c='#98B5E2',  
            #markeredgecolor = '#1A3F7A', 
            #c='#98B5E2',  
            c=scale_light_and_sat(pal_dict[par_name_for_color], 1,0.5),
            markeredgecolor = pal_dict[par_name_for_color], 
            markersize=node_size[i]/5,
            markeredgewidth = border_size[i]*1.15)
#adjust positions

pos_coeff={
'x1':[0.7,1.0],
'x2':[0.85,0.94],
'x3':[0.65,1.1],


    }

#long annotations
long_annot={}
for par in parameters:
    long_annot[par]=f"$\mathbf{{{par}}}$\n$S_1$: {si_for_plot['S1'][par]:.2f}\n$S_T$: {si_for_plot['ST'][par]:.2f}\n"
    for k,v in si_for_plot['S2'][par].items():
        if (v>index_significance_value):
            #long_annot[par]=long_annot[par]+f"$S_{{2{k}}}$: {v:.3f}\n"
            long_annot[par]=long_annot[par]+f"$S_{{2{k}↔{par}}}$: {v:.3f}\n"
for i, text in enumerate(G.nodes()):
    # if node_size[i]<100:
    #     position = (radius*1.05*np.cos(angle(Pos[text],center)), radius*1.05*np.sin(angle(Pos[text],center)))
    # else:
    #     position = (radius*1.01*np.cos(angle(Pos[text],center)), radius*1.01*np.sin(angle(Pos[text],center)))
    par_name_for_color=text.replace("(-)",'').replace(" ",'')
    position = (radius*pos_coeff[text][0]*np.cos(angle(Pos[text],center)),
                radius*pos_coeff[text][1]*np.sin(angle(Pos[text],center)))
    #plt.annotate(text, position, fontsize = 12, color='#0B2D61', family='sans-serif')
    plt.annotate(long_annot[text], position, fontsize = 13, color='0.2', family='sans-serif',va='bottom')
ax.axis('off')

fig.suptitle(f"Sobol' indices (main, total and interactions).\nIshigami function",fontsize=13,fontweight='bold',y=0.97)

#fig.tight_layout()

fig.savefig(f"14_ishigami_demo_circular_s1_s2_st.png", dpi=600)

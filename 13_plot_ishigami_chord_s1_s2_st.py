###################
# chord diagram
import os
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.colors as mpl_colors
import pickle
import numpy as np
import pandas as pd


#load demo data
data_folder='./sensitivity_results_datasets'
filename='si_ishigami_demo.pkl'
with open(os.path.join(data_folder,filename), 'rb') as handle:
    si_tmp = pickle.load(handle)
problem=si_tmp['problem']
parameters=problem['names']

s1_s2_df=pd.DataFrame(si_tmp['S2'], columns=parameters,index=parameters)
s1_s2_df=s1_s2_df.fillna(s1_s2_df.T)
st_df=pd.DataFrame(si_tmp['ST'],index=si_tmp['problem']['names'])
for i,par in enumerate(parameters):
    s1_s2_df[par][par]=si_tmp['S1'][i]


#LW = 0.3
LW = 1
# Set min index value, for the effects to be considered significant
index_significance_value = 0.001

def polar2xy(r, theta):
    return np.array([r*np.cos(theta), r*np.sin(theta)])


def IdeogramArc(start=0, end=60, radius=1.0, width=0.2, ax=None, color=(1,0,0)):
    # start, end should be in [0, 360)
    if start > end:
        start, end = end, start
    start *= np.pi/180.
    end *= np.pi/180.
    # optimal distance to the control points
    # https://stackoverflow.com/questions/1734745/how-to-create-circle-with-b%C3%A9zier-curves
    opt = 4./3. * np.tan((end-start)/ 4.) * radius
    inner = radius*(1-width)
    verts = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
        polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
        polar2xy(radius, end),
        polar2xy(inner, end),
        polar2xy(inner, end) + polar2xy(opt*(1-width), end-0.5*np.pi),
        polar2xy(inner, start) + polar2xy(opt*(1-width), start+0.5*np.pi),
        polar2xy(inner, start),
        polar2xy(radius, start),
        ]

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.LINETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CLOSEPOLY,
             ]

    if ax == None:
        return verts, codes
    else:
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.4,), lw=LW)

        ax.add_patch(patch)


def ChordArc(start1=0, end1=60, start2=180, end2=240, radius=1.0, chordwidth=0.7, ax=None, color=(1,0,0)):
    # start, end should be in [0, 360)
    if start1 > end1:
        start1, end1 = end1, start1
    if start2 > end2:
        start2, end2 = end2, start2
    start1 *= np.pi/180.
    end1 *= np.pi/180.
    start2 *= np.pi/180.
    end2 *= np.pi/180.
    opt1 = 4./3. * np.tan((end1-start1)/ 4.) * radius
    opt2 = 4./3. * np.tan((end2-start2)/ 4.) * radius
    rchord = radius * (1-chordwidth)
    verts = [
        polar2xy(radius, start1),
        polar2xy(radius, start1) + polar2xy(opt1, start1+0.5*np.pi),
        polar2xy(radius, end1) + polar2xy(opt1, end1-0.5*np.pi),
        polar2xy(radius, end1),
        polar2xy(rchord, end1),
        polar2xy(rchord, start2),
        polar2xy(radius, start2),
        polar2xy(radius, start2) + polar2xy(opt2, start2+0.5*np.pi),
        polar2xy(radius, end2) + polar2xy(opt2, end2-0.5*np.pi),
        polar2xy(radius, end2),
        polar2xy(rchord, end2),
        polar2xy(rchord, start1),
        polar2xy(radius, start1),
        ]

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ]

    if ax == None:
        return verts, codes
    else:
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.4,), lw=LW,alpha=0.3)

        ax.add_patch(patch)

def selfChordArc(start=0, end=60, radius=1.0, chordwidth=0.7, ax=None, color=(1,0,0)):
    # start, end should be in [0, 360)
    if start > end:
        start, end = end, start
    start *= np.pi/180.
    end *= np.pi/180.
    opt = 4./3. * np.tan((end-start)/ 4.) * radius
    rchord = radius * (1-chordwidth)
    verts = [
        polar2xy(radius, start),
        polar2xy(radius, start) + polar2xy(opt, start+0.5*np.pi),
        polar2xy(radius, end) + polar2xy(opt, end-0.5*np.pi),
        polar2xy(radius, end),
        polar2xy(rchord, end),
        polar2xy(rchord, start),
        polar2xy(radius, start),
        ]

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ]

    if ax == None:
        return verts, codes
    else:
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor=color+(0.5,), edgecolor=color+(0.4,), lw=LW)
        ax.add_patch(patch)

def chordDiagram(s1_s2_df,st_df,index_significance_value, ax, colors=None, width=0.1, chordwidth=0.7):

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    
    # total size in degrees
    sum_total=st_df.sum()
    st_degrees=360*st_df/sum_total
    s1_s2_degrees=s1_s2_df*float(360/sum_total)
    param_list=list(st_df.index)
    pos = {}
    #st
    arc_t = []
    arc_1 = []

    nodePos = []
    start = 0
## s1, st calculate positions
    for i,param in enumerate(param_list):
        #st
        end_t = start + float(st_degrees.loc[param])
        arc_t.append((start, end_t))
        #s1
        end_1 = start + float(s1_s2_degrees.loc[param,param])
        arc_1.append((start, end_1))
        


#### position for label
        angle = 0.5*(start+end_t)
        #print(start, end, angle)
        if -30 <= angle <= 210:
            angle -= 90
        else:
            angle -= 270
        nodePos.append(tuple(polar2xy(1.1, 0.5*(start+end_t)*np.pi/180.)) + (angle,))

#new start
        start = end_t

        
    for i,param in enumerate(param_list):
        #print (arc_t[i])
        #print (arc_1[i])
        start, end_t = arc_t[i]
        start, end_1 = arc_1[i]
        col=colors[i]

        #st plot
        IdeogramArc(start=start, end=end_t, radius=1.0, ax=ax, color=col, width=width)

        #s1 plot
        IdeogramArc(start=start, end=end_1, radius=1.0, ax=ax, color=col, width=width)
        
        
        #s2 calculate positions
        for j,param_interact in enumerate(param_list):
            
            start_inter_1 =arc_1[i][1]
            end_inter_1 = arc_1[i][1]+float(s1_s2_degrees.loc[param,param_interact])
            start_inter_2=arc_1[j][1]
            end_inter_2 = arc_1[j][1]+float(s1_s2_degrees.loc[param_interact,param])


            color = colors[i]
            # if (float(st_df.loc[param])>=float(st_df.loc[param_interact])):
            #     color = colors[i]
            # else:
            #     color=colors[j]
                

            #s2 plot
            #if (j>i) and ((float(s1_s2_df.loc[param,param_interact])>=index_significance_value) or (float(s1_s2_df.loc[param_interact,param])>=index_significance_value)):
            if ((param!=param_interact) and ((float(s1_s2_df.loc[param,param_interact])>=index_significance_value) or (float(s1_s2_df.loc[param_interact,param])>=index_significance_value))):
                #print (f'{param}<->{param_interact}:')
                #print (s1_s2_df.loc[param,param_interact])
                #print (f'start_inter_1:{start_inter_1}\nstart_inter_2:{start_inter_2}\nend_inter_1:{end_inter_1}\nend_inter_2:{end_inter_2}')
                #print ((float(s1_s2_df.loc[param,param_interact])>=index_significance_value) or (float(s1_s2_df.loc[param_interact,param])>=index_significance_value))
                ChordArc(start_inter_1, end_inter_1, start_inter_2, end_inter_2, 
                        radius=1.-width,color=colors[i],chordwidth=chordwidth, ax=ax)

    #print(nodePos)
    return nodePos

##################################

fig = plt.figure(figsize=(9,9))
#ax = plt.axes([0,0,1,1])
ax = fig.add_subplot(1,1,1)


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



custom_colors=[mpl_colors.hex2color(v) for v in pal_dict_hex.values()]






nodePos = chordDiagram(s1_s2_df,st_df,index_significance_value, ax,colors=custom_colors)
ax.axis('off')
prop = dict(fontsize=16*0.8, ha='center', va='center')


#correct_posintions


pos_corr={
    'x1':[0,0.05],
    'x2':[0,-0.15],
    'x3':[0,0]

    }




#long annotations
long_annot={}
nodePos_corr= [list(elem) for elem in nodePos]
for i,par in enumerate (parameters):
    long_annot[i]=f"$\mathbf{{{par}}}$\n$S_1$: {float(s1_s2_df.loc[par,par]):.2f}\n$S_T$: {float(st_df.loc[par]):.2f}\n"
    for k in s1_s2_df.loc[par].index:
        if ((s1_s2_df.loc[par,k]>index_significance_value)&(k!=par)):
            
            long_annot[i]=long_annot[i]+f"$S_{{2{k}↔{par}}}$: {s1_s2_df[par][k]:.3f}\n"
    nodePos_corr[i][0]=nodePos[i][0]+pos_corr[par][0]
    nodePos_corr[i][1]=nodePos[i][1]+pos_corr[par][1]


#place annotations
for i in range(len(parameters)):
    #names only
    #ax.text(nodePos[i][0], nodePos[i][1], parameters[i], rotation=nodePos[i][2], **prop)
    
    plt.annotate(long_annot[i],(nodePos_corr[i][0], nodePos_corr[i][1]), fontsize = 13, color='0.2', family='sans-serif',va='center',annotation_clip=False)

            
#    ax.text(nodePos[i][0], nodePos[i][1], long_annot[i], rotation=0, **prop)
fig.subplots_adjust(top=0.85,bottom=0.15,left=0.15,right=0.85)
fig.suptitle(f"Sobol' indices (main, total and interactions).\nIshigami function",fontsize=13,fontweight='bold',y=0.97)
fig.savefig(f"13_ishigami_demo_chord_s1_s2_st.png", dpi=600)

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns

# Célula com funções para visualização de dados

def countplot2(df,label,xticks = [],annot = True,rotation = 0,cat=False,hist = False, binwidth = None):
    fig, ax = plt.subplots()
    if hist:
        g = sns.histplot(x=label,data=df,ax=ax,binwidth=binwidth)
    else:
        g = sns.countplot(x=label, data=df, ax=ax)
    if len(xticks) == 2:
        _ = plt.xticks(xticks[0],xticks[1],rotation=rotation)
    if cat:
        max_x = len(df[label].unique()) + 1
    else:
        max_x = max(df[label])
    if annot:
        for bar in ax.get_children():
            if str(type(bar)) == "<class 'matplotlib.patches.Rectangle'>":
                if bar.get_xy()[0] < max_x and bar.get_height() > 1:
                    ax.text(math.ceil(bar.get_xy()[0]),bar.get_height()/2,'{:.1f}%'.format(bar.get_height()/len(df)*100),horizontalalignment='center',
                            color='black',fontsize='small')
    _ = plt.xticks(rotation=rotation)
    
def target(df,x,rotation=0,annot=True):
    df['count'] = 1
    aux_df = df.groupby(x).count().reset_index().sort_values(by='count',ascending=False)
    g = sns.barplot(x=x,y='count',data=aux_df)
    if annot:
        for p in g.patches:
            plt.text(p.get_x()+p.get_width()/2, p.get_y()+p.get_height()/2,str('{:.1f}%'.format(p.get_height()/len(df)*100)),
                    horizontalalignment='center',verticalalignment='center')
    plt.xticks(rotation=rotation)
        
def count_1d(df,x,hue,rotate=False):
    sns.countplot(x=x,data=df,hue=hue)
    if rotate:
        plt.xticks(rotation = 45) 
    
def describe_1d(df,x,hue,discrete=False,verbose=True):
    print_df = pd.DataFrame()
    print_df.name = 'hue'
    if discrete:
        for label in df[x].unique():
            label_df = pd.DataFrame(df.loc[df[x] == label][hue].value_counts())
            label_df.columns = [x+' '+str(label)]
            label_df = label_df/len(df.loc[df[x] == label])
            print_df = print_df.append(label_df.transpose())
        total_df = pd.DataFrame(df[x].value_counts())
        total_df.columns = ['total']
        total_df = total_df/len(df)
        cols = sorted(print_df.columns)
        print_df = print_df[cols]
        if verbose:
            display(total_df.transpose())
    else:
        for label in df[hue].unique():
            label_df = pd.DataFrame(df.loc[df[hue] == label].describe()[x])
            label_df.columns = [label]
            print_df = print_df.append(label_df.transpose())
    if verbose:
        display(print_df.transpose())
    return total_df,print_df
def kde_1d(df,x,hue,discrete=False,log=False,binwidth=3):
    fig, axes = plt.subplots(1,2,figsize=(10,6))
    if not discrete:
        sns.kdeplot(ax=axes[0],x=x,data=df,hue=hue,thresh=0,cut=0)
        axes[0].grid()
    else:
        sns.histplot(ax=axes[0],binwidth=binwidth,x=x,data=df,hue=hue,alpha=0.5)
        axes[0].grid()
    if log:
        axes[0].set_xscale('log')
    sns.boxplot(ax=axes[1],x=hue,y=x,data=df)
    
def stacked_plot(df,x,hue,annot=True,fmt=':.2f',loc=None):
    cross_tab = pd.crosstab(index=df[hue],columns=df[x],normalize="index")
    ax = cross_tab.plot(kind='bar', 
                    stacked=True, 
                    colormap='tab10')
    if loc:
        plt.legend(title=x,loc=loc)
    if annot:
        for p in ax.patches:
            plt.text(p.get_x() + p.get_width()/2, p.get_y() + p.get_height()/2,str('{:.2f}%'.format(p.get_height()*100)),
                    horizontalalignment='center',verticalalignment='center')
            
def bar_plot(df,x,hue,hue_label,y_label,split_str = ' ',annot=True,round_size=1,sort = False):
    total_df, print_df = describe_1d(df,x,hue,discrete=True)
    if sort:
        print_df = print_df.sort_values(by=hue_label,ascending=False)
    x = [i.split(split_str)[-1] for i in print_df[hue_label].index]
    fig, ax = plt.subplots()
    ax.bar(x,height=print_df[hue_label].values*100)
    plt.xticks(rotation=60)
    plt.ylabel(y_label)

    for bar in ax.get_children():
        if str(type(bar)) == "<class 'matplotlib.patches.Rectangle'>":
            if bar.get_height() > 0 and bar.get_width() == 0.8:
                _ = ax.text(math.ceil(bar.get_xy()[0]),bar.get_height()/2,'{}%'.format(round(bar.get_height(),round_size)),horizontalalignment='center',
                        color='black',fontsize='small')
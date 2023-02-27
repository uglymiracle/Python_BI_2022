import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np


def read_gff(path_to_file):
    
    names=['chromosome', 'source',
           'type', 'start', 'end', 
           'score', 'strand', 'phase',
           'attributes']
    
    gff = pd.read_csv(path_to_file, sep='\t',
                      comment='#', header=None,
                      names=names)
    
    return gff


def read_bed6(path_to_file):
    
    names=['chromosome', 'start', 'end', 
           'name', 'score', 'strand']
    
    bed6 = pd.read_csv(path_to_file, 
                       sep='\t', header=None, 
                      names=names)
    
    return bed6


df = read_gff('rrna_annotation.gff')
df.head()

#замена строк в столбце attributes
df['attributes'] = df['attributes'].str.replace(r'^Name=16S.*', '16S', regex=True) 
df['attributes'] = df['attributes'].str.replace(r'^Name=23S.*', '23S', regex=True) 
df['attributes'] = df['attributes'].str.replace(r'^Name=5S.*', '5S', regex=True) 
df.head()

df_group_rrna = df.groupby(['chromosome', 'attributes'])['attributes'].count().reset_index(name='count')

plt.subplots(figsize=(25, 10))
sns.barplot(x='chromosome', y='count', hue='attributes',data=df_group_rrna).set(xlabel='sequence')
plt.xticks(rotation=90);


#разбиение по цветам на графике
diffexpr = pd.read_table('diffexpr_data.tsv')
def map_color(df):
    logFC, Sample, log_pval = df
    
    if logFC < 0 and log_pval > 1:
        return 'Significantly downregulated'
    elif logFC < 0 and log_pval < 1:
        return 'Non-significantly downregulated'
    elif logFC > 0 and log_pval > 1:
        return 'Significantly upregulated'
    elif logFC > 0 and log_pval < 1:
        return 'Non-significantly upregulated'
    

diffexpr['color'] = diffexpr[['logFC', 'Sample', 'log_pval']].apply(map_color, axis = 1)
diffexpr.head()

texts = []

sd = diffexpr[diffexpr["color"] == 'Significantly downregulated'] #Significantly downregulated
su = diffexpr[diffexpr["color"] == 'Significantly upregulated'] #Significantly upregulated


plt.figure(figsize=(15,10))
ax = sns.scatterplot(data=diffexpr, x='logFC', y='log_pval',
                    hue='color', hue_order=['Significantly downregulated',
                                           'Significantly upregulated', 
                                           'Non-significantly downregulated',
                                           'Non-significantly upregulated'],
                    s=15, linewidth=0)

ax.axhline(1, color='gray', ls='--', lw=2)
ax.axvline(0, color='gray', ls='--', lw=2)
plt.text(7, 2, "p value = 0.05", horizontalalignment='left',
         size='large', color='grey', weight='semibold')

plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.bf'] = 'Arial:italic:bold'
plt.title('$\mathbf{Volcano}$ $\mathbf{plot}$', size=30)
plt.xlabel('$\mathbf{log_2 (fold\ change)}$', size=19)
plt.ylabel('$\mathbf{-log_{10} (p}$ $\mathbf{value\ corrected)}$', size=19)
ax.minorticks_on()
plt.xticks(np.arange(-10, 11, 5.0), size=10, weight='semibold')
plt.yticks(np.arange(0, 110, 20.0), size=10, weight='semibold')

#подсчет чисел для лимитов
x_min = min(diffexpr['logFC'])
x_max = max(diffexpr['logFC'])
limit = max(abs(x_min), abs(x_max)) + 1
plt.xlim([-limit, limit])

#смена толщины осей
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.5)
    
#легенда
plt.legend(prop={'weight': 'bold', 
                 'family': 'Sans-serif',
                'size': 12},
          markerscale=2.0, shadow=True)

#аннотация
for i in range(len(su)):
    if su.iloc[i].logFC == max(su.logFC):

        ax.annotate(su.iloc[i].Sample,
            xy=(su.iloc[i].logFC, su.iloc[i].log_pval),
            xytext=(su.iloc[i].logFC+3, su.iloc[i].log_pval+3),
            va='center',
            ha='center',
            arrowprops={'facecolor':'red', 'shrink':0.05},
                   weight='bold')
        
        su.iloc[i,1] = 0
        break
        
for i in range(len(su)):
    if su.iloc[i].logFC == max(su.logFC):
        ax.annotate(su.iloc[i].Sample,
            xy=(su.iloc[i].logFC, su.iloc[i].log_pval),
            xytext=(su.iloc[i].logFC, su.iloc[i].log_pval+10),
            va='center',
            ha='center',
            arrowprops={'facecolor':'red', 'shrink':0.05},
                   weight='bold')

for j in range(len(sd)):
    if sd.iloc[j].logFC == min(sd.logFC):
        ax.annotate(sd.iloc[j].Sample,
            xy=(sd.iloc[j].logFC, sd.iloc[j].log_pval),
            xytext=(sd.iloc[j].logFC, sd.iloc[j].log_pval+7),
            va='center',
            ha='center',
            arrowprops={'facecolor':'red', 'shrink':0.05},
                   weight='bold')
        sd.iloc[j,1] = 0
        break
        
for j in range(len(sd)):
    if sd.iloc[j].logFC == min(sd.logFC):
        ax.annotate(sd.iloc[j].Sample,
            xy=(sd.iloc[j].logFC, sd.iloc[j].log_pval),
            xytext=(sd.iloc[j].logFC-2, sd.iloc[j].log_pval+3),
            va='center',
            ha='center',
            arrowprops={'facecolor':'red', 'shrink':0.05},
                   weight='bold');





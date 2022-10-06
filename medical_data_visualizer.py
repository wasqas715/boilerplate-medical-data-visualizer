import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



# id,age,sex,height,weight,ap_hi,ap_lo,cholesterol,gluc,smoke,alco,active,cardio
# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
# using np.where
# df_x = np.where(x, a, y) == dataframe to look in = np.where(if i statisfies the function/inequality of x, apply a to i, else apply y)
df["overweight"] = np.where(df['weight'] / ((df['height'] / 100) ** 2) > 25, 1, 0)
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
# Using np.where
df["cholesterol"] = np.where(df["cholesterol"] == 1, 0, 1)
df["gluc"] = np.where(df["gluc"] == 1, 0, 1)


# Draw Categorical Plot
def draw_cat_plot():
    cat_options = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat =  df.melt(id_vars=["cardio"], value_vars=cat_options)


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # df_cat["total"]=1
    # df_cat = df_cat.groupby(["variable", "cardio", "value"], as_index=False).count()
    

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable', hue='value', col='cardio', data = df_cat, kind='count', palette='Blues')


    # Get the figure for the output
    fig.set_axis_labels("variable", "total")
    fig = fig.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) 
        & (df["height"] >= df["height"].quantile(0.025)) 
        & (df["height"] <= df["height"].quantile(0.975)) 
        & (df["weight"] >= df["weight"].quantile(0.025)) 
        & (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    # creating mask
    mask = np.triu(np.ones_like(df_heat.corr()))



    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'

    ax = sns.heatmap(corr, mask=mask, ax=ax, annot=True, fmt=".1f")
    # fig = heat_table.figure
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig

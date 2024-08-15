import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import the data from medical_examination.csv and assign it to the df variable
df = pd.read_csv('medical_examination.csv')

# Create the overweight column in the df variable
df['BMI'] = round(((df['weight']) / (df['height'] / 100) ** 2), 2)
df['overweight'] = df['BMI'].apply(lambda x: 1 if x > 25 else 0)

# Normalize data by making 0 always good and 1 always bad. 
df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)

# Draw the Categorical Plot in the draw_cat_plot function
def draw_cat_plot():
    # Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature.
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).count()
    df_cat = df_cat.rename(columns={'total': 'total'})  # Keep 'total' to match test case

    # Create the catplot
    cat_plot = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar', height=5, aspect=1.2)

    # Get the figure for the output and store it in the fig variable
    fig = cat_plot.fig

    plt.show()

# Draw the Heat Map in the draw_heat_map function
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Remove the 'BMI' column since the test expects 'overweight'
    df_heat = df_heat.drop(columns=['BMI'])

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot the heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', square=True, linewidths=0.5, cbar_kws={"shrink": .5}, vmin=-0.1, vmax=0.8)

    plt.show()

def validate_option(message=": ",max_option=1):
  while True:
    option_=input(message)
    try: 
      if int(option_)<=max_option and int(option_)>0:
        break
    except:
      print("===Input a valid option===")
  return option_

while True:
  print("Chose your chart from the menu:")
  option=validate_option("1 for categorical plot . \n2 for heat map.\n3 EXIT.\n: ",3)

  if option=="1":
     draw_cat_plot()
  if option=="2":
     draw_heat_map()
  if option=="3":
     break





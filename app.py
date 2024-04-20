import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os


st.title("🍁Decoding Canada's Evolving Job Market")

st.subheader("💵Analyzing the data on Canadian wages")
st.markdown("In analyzing the data on Canadian wages, it is evident that there are notable trends to consider. Firstly, when examining the overall wage trends over time, it is observed that Engineering Professionals stand out with higher wages compared to other professions. However, the wage increase for each job category remains relatively aligned over time, indicating a consistent growth pattern across various sectors. This suggests a stable and balanced wage growth trajectory across different professions in Canada.")
df = pd.read_csv('dataset/Average_Hourly_Wages_Overall_Canadian.csv', sep='\t')
#st.write(df.head())
# Compare the overall hourly wage trend (total employees) against health and engineering professionals
# Filter the DataFrame for the selected occupations
selected_occupations = df[df['National Occupational Classification (NOC)'].isin(['Professional occupations in engineering [213]', 'Professional occupations in health [31]', 'Total employees, all occupations [00-95]'])]
# Create a line plot
fig = plt.figure(figsize=(10, 6))
sns.lineplot(x='REF_DATE', y='VALUE', hue='National Occupational Classification (NOC)', data=selected_occupations, marker='o')
plt.title('Comparison of NOC over Years')
plt.xlabel('Year')
plt.ylabel('Average Hourly Wage')
plt.grid(True)
plt.show()
st.pyplot(fig)


# Compare the average weekly wage between full-time and part-time employees. Use a bar chart to for visualization
# Hint: You may need to filter the dataframe based on the 'Type of work' column and then use groupby and mean to calculate the average wages.
# Calculation method: Find the average between all the available years in the dataset for both type of work
st.subheader("⌛Employment type and hourly wages rate")
st.markdown("Exploring the employment types sheds light on disparities in earnings, particularly in relation to financial stability and hourly rates. The data indicates that individuals in management and professional occupations tend to earn more compared to workers in labor-intensive roles. This disparity in earnings underscores the impact of job type and industry on financial stability, highlighting the importance of addressing wage gaps and ensuring fair compensation across all employment sectors. By delving into these key aspects of Canadian wages, a comprehensive understanding of the wage landscape emerges, emphasizing the need for continued analysis and action to promote equitable pay practices and financial security for all workers.")
df_fulltime = pd.read_csv('dataset/Average_Weekly_Wages_Full-time_Canadian.csv', sep=',')
df_partime = pd.read_csv('dataset/Average_Weekly_Wages_Part-time_Canadian.csv', sep=',')
df_fulltimepartime = pd.concat([df_fulltime, df_partime])
df_fulltimepartimegroup = df_fulltimepartime.groupby(['REF_DATE', 'Type of work'])['VALUE'].mean().rename("Average Wage").reset_index()

# Create Visualization
fig = plt.figure(figsize=(10, 6))
ax = sns.barplot(df_fulltimepartimegroup, x="REF_DATE", y="Average Wage", hue="Type of work")
# Add labels to the bars
for l in ax.containers:
  ax.bar_label(l, fmt='%.2f', fontsize=7.5, padding=1)
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))
plt.xlabel("Year")
plt.ylabel("Average Weekly Wage")
plt.title("Average Weekly Wage over Years")
plt.show()
st.pyplot(fig)

# Identify the top 5 occupations with the highest average wage
# Plot a heatmap of those top 5 occupations average wages by occupation and age group to visualize the distribution across these dimensions.
# Hint: Group the data by 'National Occupational Classification (NOC)' and calculate the mean wage. Then sort the results and use head() to get the top 5 occupations.

# Compare the bottom 3 and top 3 occupations for the average hourly wage between sexes. Provide 2 boxplots, separating the top and bottom occupations
# Hint: The boxplot should indicate the distributions over time, and make inferences about the
df_topoccupation = pd.read_csv('dataset/Average_Hourly_Wages_Overall_Canadian.csv', sep='\t')

df_topoccupation_group = df_topoccupation.groupby(['National Occupational Classification (NOC)','Age group'])['VALUE'].mean().reset_index()
df_topoccupation_group_sort = df_topoccupation_group.sort_values('VALUE', ascending=False).head()

# load data
heatmap_data = df_topoccupation_group_sort.pivot(index="National Occupational Classification (NOC)", columns="Age group", values="VALUE")

# create visualization
plt.figure(figsize=(10, 6))  # Set the figure size
plt.xlabel("Age group")
plt.ylabel("Occupation")
plt.title("Average Hourly Wages by Occupation and Age Group")
sns.heatmap(heatmap_data, annot=True)
plt.show()
st.pyplot(plt)




# Compare the bottom 3 and top 3 occupations for the average hourly wage between sexes. Provide 2 boxplots, separating the top and bottom occupations
# Hint: The boxplot should indicate the distributions over time, and make inferences about the
st.subheader("👫Gender & Wage Disparity")
st.markdown("Moving on to the gender wage difference, a significant issue of pay equity between men and women is highlighted. The data reveals that men tend to earn higher wages than women in the same occupations, particularly in the top occupation categories. This disparity underscores the ongoing challenge of achieving gender pay equity in the Canadian workforce, emphasizing the need for continued efforts to address and rectify these discrepancies.")

df_male = pd.read_csv('dataset/Average_Hourly_Wages_Male_Canadian.csv', sep=',')
df_female = pd.read_csv('dataset/Average_Hourly_Wages_Female_Canadian.csv', sep=',')

####create empty dataframe (Male)
df_male_top3 = pd.DataFrame(columns=df_male.columns) # top 3 each year
df_male_bottom3 = pd.DataFrame(columns=df_male.columns) # bottom 3 each year

df_male_group = df_male.groupby(['REF_DATE', 'National Occupational Classification (NOC)', 'Sex'])['VALUE'].mean().reset_index()
for year in df_male_group['REF_DATE'].unique():
    df_male_top3 = pd.concat([df_male_top3, df_male_group[df_male_group['REF_DATE'] == year].sort_values('VALUE') .tail(3)])
    df_male_bottom3 =pd.concat([df_male_bottom3, df_male_group[df_male_group['REF_DATE'] == year].sort_values('VALUE') .head(3)])
df_male_top3.sort_values('REF_DATE')  
df_male_bottom3.sort_values('REF_DATE')  


####create empty dataframe (Female)
df_female_top3 = pd.DataFrame(columns=df_female.columns) # top 3 each year
df_female_bottom3 = pd.DataFrame(columns=df_female.columns) # bottom 3 each year

df_female_group = df_female.groupby(['REF_DATE', 'National Occupational Classification (NOC)', 'Sex'])['VALUE'].mean().reset_index()
for year in df_female_group['REF_DATE'].unique():
    df_female_top3 = pd.concat([df_female_top3, df_female_group[df_female_group['REF_DATE'] == year].sort_values('VALUE') .tail(3)])
    df_female_bottom3 =pd.concat([df_female_bottom3, df_female_group[df_female_group['REF_DATE'] == year].sort_values('VALUE') .head(3)])
df_female_top3.sort_values('REF_DATE')  
df_female_bottom3.sort_values('REF_DATE')  

### concat dataframe
df_gender_all_top3 = pd.concat([df_male_top3, df_female_top3 ])
df_gender_all_bottom = pd.concat([df_male_bottom3, df_female_bottom3 ])

### boxplot
# Create two boxplots
axes = plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
box_plottop = sns.boxplot(data=df_gender_all_top3, x="REF_DATE", y="VALUE", hue="Sex")
plt.title("Top 3 Occupations over year between sexes")

plt.subplot(1, 2, 2)
box_plotbottom = sns.boxplot(data=df_gender_all_bottom, x="REF_DATE", y="VALUE", hue="Sex")
plt.title("Bottom 3 Occupations over year between sexes")

box_plottop.set(xlabel='Year', ylabel = 'Average Hourly Wages')
box_plotbottom.set(xlabel='Year', ylabel = 'Average Hourly Wages')

plt.tight_layout()
plt.show()

st.pyplot(plt)


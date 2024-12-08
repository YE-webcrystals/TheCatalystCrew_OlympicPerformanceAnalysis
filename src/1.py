import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st


athlete_df = pd.read_csv('athlete_events.csv')                         # Load data
noc_df = pd.read_csv('noc_regions.csv')                                # Load data
                                                           

athlete_df = athlete_df[athlete_df['Season'] == 'Summer']              # Filter only Summer Olympics data

df = athlete_df.merge(noc_df, on='NOC', how='left')                    # Merge with NOC region data

medal_df = pd.get_dummies(df['Medal'])                                 # One-hot encode Medal column
df = pd.concat([df, medal_df], axis=1)

df.drop_duplicates(inplace=True)                                       # Drop duplicates

def total_medals_by_country(df):
    medal_tally = df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].reset_index()               # Group data by 'region' and sum up the medal counts for 'Gold', 'Silver', and 'Bronze'.
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']         # Add a new column 'Total' that calculates the total medal count for each region.
    medal_tally = medal_tally.sort_values(by='Gold', ascending=False)                                  # Sort the DataFrame by the number of gold medals in descending order.
    return medal_tally

medal_tally = total_medals_by_country(df)                 # Call the function `total_medals_by_country` to calculate the total medal tally by region
# and store the resulting DataFrame in the variable `medal_tally`.
print(medal_tally.head())            # Print the first 5 rows of the `medal_tally` DataFrame to display a quick summary of the top regions.

def most_successful_athletes(df):                          # Filter out rows where the 'Medal' column has NaN values (non-medal winners).
    medal_winners = df.dropna(subset=['Medal'])            
    top_athletes = (                                       # Count the number of medals won by each athlete, sort in descending order,# and take the top 10 athletes.
        medal_winners['Name']                              # Select the 'Name' column
        .value_counts()                                    # Count the occurrences of each athlete's name
        .head(10)                                          # Get the top 10 athletes
        .reset_index()                                     # Reset the index to turn it into a DataFrame
        .rename(columns={'index': 'Athlete', 'Name': 'Medals'})             # Rename columns for clarity
    )
    return top_athletes

top_athletes = most_successful_athletes(df)           # Call the `most_successful_athletes` function to get the top 10 athletes based on the number of medals won.
# Store the resulting DataFrame in the variable `top_athletes`.
print(top_athletes)                                       # Print the `top_athletes` DataFrame to display the names of the top athletes and their respective medal counts.

def medals_over_time(df, medal_type='Gold'):           # Function to calculate the total medals of a specified type over time
    medals = df.groupby('Year').sum()[medal_type].reset_index()        # Group data by 'Year' and calculate the sum of the specified medal type for each year.
    return medals

gold_medals = medals_over_time(df, 'Gold')              # Get the total number of gold medals over time.
print(gold_medals.head())                               # Print the first 5 rows of the DataFrame showing the trend of gold medals over the years.

def top_sports(df):                                     # Function to find the top 10 sports based on the total number of medals won.
    sport_medals = df['Sport'].value_counts().head(10).reset_index()            # Count the number of medals for each sport, sort in descending order, and take the top 10.
    sport_medals.columns = ['Sport', 'Medals']            # Rename the columns for better readability.
    return sport_medals

sports = top_sports(df)
print(sports)

medal_tally = total_medals_by_country(df)
top_countries = medal_tally.head(10)                                           # Get the top 10 countries

st.title('Olympics Medal Analysis')                                            # Streamlit App - Set up the title
medal_tally = total_medals_by_country(df)

# Display Medal Tally DataFrame
st.dataframe(medal_tally)

selected_country = st.selectbox('Select Country', medal_tally['region'])       # Select country dropdown
country_data = medal_tally[medal_tally['region'] == selected_country]
st.write(f"Medals for {selected_country}")
st.write(country_data)

st.subheader('Gold Medals Over Time')                                    # --- =Graph 1: Gold Medals Over Time (Matplotlib) ---
plt.figure(figsize=(10, 6))
plt.plot(gold_medals['Year'], gold_medals['Gold'], marker='o')
plt.title('Gold Medals Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Gold Medals')
plt.grid()
st.pyplot(plt)

st.subheader('Top 10 Sports by Medal Count')                             # --- Graph 2: Top 10 Sports by Medal Count (Seaborn) ---
plt.figure(figsize=(10, 6))
sns.barplot(x='Medals', y='Sport', data=sports, palette='magma')
plt.title('Top 10 Sports by Medal Count')
plt.xlabel('Medal Count')
plt.ylabel('Sport')
st.pyplot(plt)

st.subheader('Interactive Plot of Top 10 Countries by Total Medals:')         # --- Graph 3: Interactive Plot (Plotly) ---
fig = px.bar(top_countries, x='Total', y='region', title='Top 10 Countries by Total Medals')
st.plotly_chart(fig)

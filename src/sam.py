from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator

# declarative base class
Base = declarative_base()

# create engine
engine = create_engine('sqlite:///data/vivino.db')

# create session
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

# SQL queries
# Question 1
# We have a marketing budget for this year. Which country should we prioritise and why?
# Least users = more room to grow
question2query1 = text("""
             SELECT  
             countries.name, countries.users_count        
             FROM countries
             order by countries.users_count desc
             LIMIT 5;
             """
             )
# Most users = Keep focusing on growing largest users
question2query2 = text("""
             SELECT  
             countries.name, countries.users_count         
             FROM countries
             GROUP BY countries.name
             order by countries.users_count asc
             LIMIT 5;
             """
             )

# Focus on countries with most sales
question2query3 = text("""
             SELECT  
             countries.name, sum(vintages.price_euros) AS total_sold        
             FROM countries
             JOIN regions on regions.country_code = countries.code
             JOIN wines on wines.region_id = regions.id
             JOIN vintages on vintages.wine_id = wines.id
             GROUP BY countries.name
             order by sum(vintages.price_euros) desc
             LIMIT 5;
             """
             )

# Least sales = more room to grow
question2query4 = text("""
             SELECT  
             countries.name, sum(vintages.price_euros) AS total_sold          
             FROM countries
             JOIN regions on regions.country_code = countries.code
             JOIN wines on wines.region_id = regions.id
             JOIN vintages on vintages.wine_id = wines.id
             GROUP BY countries.name
             order by sum(vintages.price_euros) asc
             LIMIT 5;
             """
             )

# Question 2
# We have detected that a big cluster of customers like a specific combination of tastes. 
# We have identified a few `primary` `keywords` that match this. 
# We would like you to **find all the wines that have those keywords**. 
# To ensure the accuracy of our selection, ensure that **more than 10 users confirmed those keywords**. Also, identify the `group_name` related to those keywords.
question4query1 = text("""
            SELECT   
                wines.name as wine_name,
                GROUP_CONCAT(' ' || keywords.name || ' (' || keywords_wine.group_name || ')') as flavor
            FROM 
                wines
            JOIN keywords_wine on keywords_wine.wine_id = wines.id
            JOIN keywords on keywords.id = keywords_wine.keyword_id
            WHERE 
                keywords.name in ('coffee', 'toast', 'green apple', 'cream', 'citrus') AND keywords_wine.keyword_type = 'primary' AND keywords_wine.count > 10
            GROUP BY
                wines.name
            HAVING
                COUNT(keywords.name in ('coffee', 'toast', 'green apple', 'cream', 'citrus') AND keywords_wine.keyword_type = 'primary' AND keywords_wine.count > 10) > 1
            ORDER BY
                wines.name;
             """
             )
question4query2 = text("""
            SELECT   
                wines.name as wine_name,
                keywords_wine.group_name as flavor_group
            FROM 
                wines
            JOIN keywords_wine on keywords_wine.wine_id = wines.id
            JOIN keywords on keywords.id = keywords_wine.keyword_id
            WHERE 
                keywords.name in ('coffee', 'toast', 'green apple', 'cream', 'citrus') AND keywords_wine.count > 10 AND keywords_wine.keyword_type = 'primary'
            ORDER BY
                wines.name;
             """
             )

question4query3 = text("""
            SELECT   
                keywords_wine.group_name,
                count(wines.id) as count
            FROM 
                wines
            JOIN keywords_wine on keywords_wine.wine_id = wines.id
            JOIN keywords on keywords.id = keywords_wine.keyword_id
            JOIN vintages on wines.id = vintages.wine_id
            WHERE 
                keywords.name in ('coffee', 'toast', 'green apple', 'cream', 'citrus') AND keywords_wine.keyword_type = 'primary' AND keywords_wine.count > 10
            GROUP BY
                keywords_wine.group_name;
             """
             )

# fetch data from db
# Question 1
df1 = pd.read_sql((question2query1), engine)
df2 = pd.read_sql((question2query2), engine)
df3 = pd.read_sql((question2query3), engine)
df4 = pd.read_sql((question2query4), engine)
# Question 2
df5 = pd.read_sql((question4query2), engine)
df6 = pd.read_sql((question4query1), engine)

# Question 1
plt.rcParams.update({'font.size': 20})

fig1, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))

ax1 = axes[0, 0]
ax1.plot(df1.name, df1.users_count)
ax1.set_title('Highest amount of users')
ax1.set_ylabel('Users Count')
ax1.yaxis.set_minor_formatter(ScalarFormatter())
ax1.set_xticklabels(df1.name, rotation=45, ha="right")
ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))
ax1.yaxis.set_minor_formatter(ScalarFormatter())
ax1.ticklabel_format(style='plain', axis='y')

ax2 = axes[0, 1]
ax2.plot(df2.name, df2.users_count)
ax2.set_title('Least amount of users')
ax2.set_ylabel('Users Count')
ax2.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax2.set_xticklabels(df2.name, rotation=45, ha="right")

ax3 = axes[1, 0]
ax3.plot(df3.name, df3.total_sold)
ax3.set_title('Most sales')
ax3.set_ylabel('Total Sales Volume')
ax3.set_xticklabels(df3.name, rotation=45, ha="right")
ax3.yaxis.set_major_locator(MaxNLocator(nbins=5))

ax4 = axes[1, 1]
ax4.plot(df4.name, df4.total_sold)
ax4.set_title('Lowest sales')
ax4.set_ylabel('Total Sales Volume')
ax4.set_xticklabels(df4.name, rotation=45, ha="right")
ax4.yaxis.set_major_locator(MaxNLocator(nbins=5))

fig1.suptitle("Countries to focus our marketing budget on", fontsize=40)
fig1.tight_layout()

# Question 2
# Count the occurrence of each flavor group for each wine
flavor_group_counts = df5['flavor_group'].value_counts()

# Create the bar plot
plt.figure(figsize=(10, 6))
flavor_group_counts.plot(kind='bar')
plt.xlabel('')
plt.ylabel('Number of Wines')
plt.title('Number of Wines for each Flavor Group (Primary)')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
fig2 = plt.gcf()


st.pyplot(fig1.figure)
st.write(" ")
st.pyplot(fig2)
st.header("Dynamic Flavor Selection")

# Options for filtering
filter_options = ['coffee', 'toast', 'green apple', 'cream', 'citrus']

# Multiselect for selecting flavors
selected_keywords = st.multiselect("Select Flavor(s)", filter_options)

# Filter the data based on selected keywords
filtered_df = df6[df6['flavor'].apply(lambda x: all(keyword in x for keyword in selected_keywords))]

# Display the filtered results as a dynamic list
if not filtered_df.empty:
    st.subheader("Filtered Results")
    for idx, row in filtered_df.iterrows():
        st.write(f"**Wine Name:** {row['wine_name']}")
        st.write(f"**Flavors:** {row['flavor']}")
        st.write(" ")
else:
    st.write("No results match the selected keywords.")
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

# SQL query
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

# We have detected that a big cluster of customers like a specific combination of tastes. 
# We have identified a few `primary` `keywords` that match this. 
# We would like you to **find all the wines that have those keywords**. 
# To ensure the accuracy of our selection, ensure that **more than 10 users confirmed those keywords**. Also, identify the `group_name` related to those keywords.
question4query1 = text("""
            SELECT   
                vintages.name,
                wines.name,
                group_concat(distinct(keywords_wine.group_name))
            FROM 
                wines
            JOIN keywords_wine on keywords_wine.wine_id = wines.id
            JOIN keywords on keywords.id = keywords_wine.keyword_id
            JOIN vintages on wines.id = vintages.wine_id
            WHERE 
                keywords.name in ('coffee', 'toast', 'green apple', 'cream', 'citrus') AND keywords_wine.count > 10
            GROUP BY
                vintages.name
            HAVING
                COUNT(keywords.name in ('coffee', 'toast', 'green apple', 'cream', 'citrus') AND keywords_wine.count > 10) > 1
            ORDER BY
                wines.name;
             """
             )

# fetch data from db
results1 = session.execute(question2query1)
results2 = session.execute(question2query2)
results3 = session.execute(question2query3)
results4 = session.execute(question2query4)
results5 = session.execute(question4query1)


df1 = pd.read_sql((question2query1), engine)
df2 = pd.read_sql((question2query2), engine)
df3 = pd.read_sql((question2query3), engine)
df4 = pd.read_sql((question2query4), engine)
df5 = pd.read_sql((question4query1), engine)

#df1.index += 1

M = 5

#fig = plt.figure(df1)
plt.rcParams.update({'font.size': 20})

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12))

ax1 = axes[0, 0]
ax1.plot(df1.name, df1.users_count)
ax1.set_title('Highest amount of users')
ax1.set_xlabel('Name')
ax1.set_ylabel('Users Count')
ax1.yaxis.set_minor_formatter(ScalarFormatter())
ax1.set_xticklabels(df1.name, rotation=45, ha="right")
ax1.yaxis.set_major_locator(MaxNLocator(nbins=5))
ax1.yaxis.set_minor_formatter(ScalarFormatter())
ax1.ticklabel_format(style='plain', axis='y')

ax2 = axes[0, 1]
ax2.plot(df2.name, df2.users_count)
ax2.set_title('Least amount of users')
ax2.set_xlabel('Name')
ax2.set_ylabel('Users Count')
ax2.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
ax2.set_xticklabels(df1.name, rotation=45, ha="right")

ax3 = axes[1, 0]
ax3.plot(df3.name, df3.total_sold)
ax3.set_title('Most sales')
ax3.set_xlabel('Name')
ax3.set_ylabel('Total Sold')
ax3.set_xticklabels(df1.name, rotation=45, ha="right")
ax3.yaxis.set_major_locator(MaxNLocator(nbins=5))

ax4 = axes[1, 1]
ax4.plot(df4.name, df4.total_sold)
ax4.set_title('Lowest sales')
ax4.set_xlabel('Name')
ax4.set_ylabel('Total Sold')
ax4.set_xticklabels(df1.name, rotation=45, ha="right")
ax4.yaxis.set_major_locator(MaxNLocator(nbins=5))

fig.tight_layout()

st.pyplot(fig.figure)

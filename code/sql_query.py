from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

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
             countries.name, sum(vintages.price_euros)          
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
             countries.name, sum(vintages.price_euros)          
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
                group_concat(keywords_wine.group_name, ', ')
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
                COUNT(keywords.name) > 1
            ORDER BY
                wines.name;
             """
             )

"""coffee
toast
green apple
cream
citrus"""
# fetch data from db
results = session.execute(question4query1)

# print results
for result in results:
    print(result)



""" JOIN toplists on countries.code = toplists.country_code
             JOIN regions on countries.code = regions.country_code
             JOIN wines on regions.id = wines.region_id
             JOIN most_used_grapes_per_country on regions.country_code = most_used_grapes_per_country.country_code
             JOIN toplists on toplists.country_code = countries.code
             JOIN vintage_toplists_rankings on vintage_toplists_rankings.id = toplists.id
query = text(
             SELECT  
             countries.name, countries.users_count, sum(vintages.price_euros)          
             FROM vintage_toplists_rankings
             JOIN vintages on vintages.id = vintage_toplists_rankings.vintage_id
             JOIN toplists on toplists.id = vintage_toplists_rankings.top_list_id
             JOIN wines on wines.id = vintages.wine_id
             JOIN regions on regions.id = wines.region_id
             JOIN countries on countries.code = regions.country_code
             JOIN most_used_grapes_per_country on most_used_grapes_per_country.country_code = countries.code
             JOIN grapes on grapes.id = most_used_grapes_per_country.grape_id
             GROUP BY countries.name
             order by countries.users_count desc
             LIMIT 5;
             """
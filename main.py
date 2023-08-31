import src.queries as queries
import streamlit as st
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# declarative base class
Base = declarative_base()

# create engine
engine = create_engine('sqlite:///data/vivino.db')

# create session
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

# connecting database
connection = sqlite3.connect('./data/vivino_new.db')
cursor = connection.cursor()

st.set_page_config(page_title = 'vivino', page_icon = '🍷')
st.title ('')

choice = st.sidebar.radio('Choose one to visualise',['Contents',
                                            'Top 5 grapes in each countries',
                                            'Total wines count of each countries', 
                                            'Ratings of top 15 wines',
                                            'Marketing budget', 
                                            'Wines per flavor',
                                            'Top 10 wines',
                                            'Average rating per country',
                                            'Average rating by year',
                                            'Top 5 for VIP',
                                            'The End'
                                            ])
st.write(" ")
st.write(" ")

if choice == 'Contents':
    st.title('Visualisation on Vivino')
    st.subheader('About wine :')
    st.write("Wine is enjoyed all around the world for a variety of reasons. Whether you like to drink it alongside your favourite meal at a restaurant, or as a stress relief from a long, tiring week, there is no right or wrong occasion to indulge in this delicious beverage. With so many types and brands to choose from, there is something for everyone 🍷")
    st.subheader('About visualisation on Vivino :')
    st.write('* With the data provided by Vivino, we provide few visualisation to get to know the data in a better way.\n* Through `>`in left top corner you can access the list of visualisation.')
elif choice == 'Top 5 grapes in each countries':
    queries.heatmap_for_grape(cursor)
elif choice == 'Total wines count of each countries':
    queries.barchart_for_countries_WinesVintageCount(cursor)
elif choice == 'Ratings of top 15 wines':
    queries.ratings_of_top15wines(cursor)
elif choice == 'Marketing budget':
    queries.marketing_budget(engine)
elif choice == 'Wines per flavor':
    queries.wine_flavor(engine)
elif choice == 'Top 10 wines':
    queries.top_ten_wines()
elif choice == 'Average rating per country':
    queries.rating_by_country()
elif choice == 'Average rating by year':
    queries.rating_by_year()
elif choice == 'Top 5 for VIP':
    queries.vip()
elif choice == 'The End':
    queries.end()

# closing vivino_new.db connections
cursor.close()
connection.close()

# closing vivino.db session
session.close()
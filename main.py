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
st.title ('Visualisation on Vivino')
choice = st.sidebar.radio('Choose one to visualise',['Contents',
                                            'Usage of top 5 grapes accross countries',
                                            'Wines, Vintage and total wines count of each countries', 
                                            'Ratings of top 15 wines',
                                            'Marketing budget', 
                                            'Wines per flavor'
                                            ])
st.write(" ")
st.write(" ")
if choice == 'Usage of top 5 grapes accross countries':
    queries.heatmap_for_grape(cursor)
elif choice == 'Wines, Vintage and total wines count of each countries':
    queries.barchart_for_countries_WinesVintageCount(cursor)
elif choice == 'Ratings of top 15 wines':
    queries.ratings_of_top15wines(cursor)
elif choice == 'Marketing budget':
    queries.marketing_budget(engine)
elif choice == 'Wines per flavor':
    queries.wine_flavor(engine)

# closing vivino_new.db connections
cursor.close()
connection.close()

# closing vivino.db session
session.close()

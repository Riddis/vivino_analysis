import code.queries as queries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import streamlit as st
import sqlite3

# declarative base class
Base = declarative_base()

# create engine
engine = create_engine('sqlite:///data/vivino.db')

# create session
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

connection = sqlite3.connect('./data/vivino.db')
cursor = connection.cursor()

st.set_page_config(page_title = 'vivino', page_icon = '🍷')
st.title ('Visualisation on Vivino')
choice = st.radio('Choose one to visualise',[
                                            'Usage of top 5 grapes accross countries',
                                            'Wines, Vintage and total wines count of each countries', 
                                            'Marketing budget', 
                                            'Wines per flavor'
                                            ])

if choice == 'Usage of top 5 grapes accross countries':
    queries.heatmap_for_grape(cursor)
elif choice == 'Wines, Vintage and total wines count of each countries':
    queries.barchart_for_countries_WinesVintageCount(cursor)
elif choice == 'Marketing budget':
    queries.marketing_budget(engine)
elif choice == 'Wines per flavor':
    queries.wine_flavor(engine)
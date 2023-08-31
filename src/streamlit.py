import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('../vivino.db')
cursor = connection.cursor()

st.set_page_config(page_title = 'vivino', page_icon = '🍷')
st.title ('Visualisation on Vivino')


def heatmap_for_grape():
    st.header('Usage of top 5 grapes accross countries')

    queries = {
    'Cabernet Sauvignon': """
        SELECT countries.name
        FROM countries
        JOIN most_used_grapes_per_country ON most_used_grapes_per_country.country_code = countries.code
        JOIN grapes ON grapes.id = most_used_grapes_per_country.grape_id
        WHERE grapes.name = 'Cabernet Sauvignon'
    """,
    'Chardonnay': """
        SELECT countries.name
        FROM countries
        JOIN most_used_grapes_per_country ON most_used_grapes_per_country.country_code = countries.code
        JOIN grapes ON grapes.id = most_used_grapes_per_country.grape_id
        WHERE grapes.name = 'Chardonnay'
    """,
    'Pinot Noir': """
        SELECT countries.name
        FROM countries
        JOIN most_used_grapes_per_country ON most_used_grapes_per_country.country_code = countries.code
        JOIN grapes ON grapes.id = most_used_grapes_per_country.grape_id
        WHERE grapes.name = 'Pinot Noir'
    """,
    'Merlot': """
        SELECT countries.name
        from countries
        JOIN most_used_grapes_per_country ON most_used_grapes_per_country.country_code = countries.code
        JOIN grapes ON grapes.id = most_used_grapes_per_country.grape_id
        WHERE grapes.name = 'Merlot'
    """,
    'Shiraz/Syrah':  """
        SELECT countries.name
        from countries
        JOIN most_used_grapes_per_country ON most_used_grapes_per_country.country_code = countries.code
        JOIN grapes ON grapes.id = most_used_grapes_per_country.grape_id
        WHERE grapes.name = 'Shiraz/Syrah'
    """

    }

    data = []
    for grape_variety, query in queries.items():
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            data.append((grape_variety, row[0]))

    df = pd.DataFrame(data, columns=['Grape Variety', 'Country'])

    # Reshape the DataFrame using pivot_table
    df_pivot = pd.pivot_table(df, index='Grape Variety', columns='Country', aggfunc=len, fill_value=0)

    # Create the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_pivot, annot=True, cmap='YlGnBu', cbar=False)

    # Set the title and labels
    plt.title("Countries associated with Grape Varieties")
    plt.xlabel("Country")
    plt.ylabel("Grape Variety")

    # Display the chart
    st.pyplot(plt)

def barchart_for_countries_WinesVintageCount():
    st.header('Wines, Vintage and total wines count of each countries')

    list_of_countries = []
    for x in cursor.execute('''SELECT name FROM countries'''):
        list_of_countries.append(x[0])

    data = []

    for country in list_of_countries:
        query1 = f'''
        SELECT COUNT(DISTINCT vintages.name)
        FROM countries
        JOIN regions ON regions.country_code = countries.code
        JOIN wines ON wines.region_id = regions.id
        JOIN vintages ON vintages.wine_id = wines.id
        WHERE countries.name = '{country}'
        '''

        query2 = f'''
        SELECT COUNT(DISTINCT wines.name)
        FROM countries
        JOIN regions ON regions.country_code = countries.code
        JOIN wines ON wines.region_id = regions.id
        WHERE countries.name = '{country}'
        '''

        wine_count = 0
        vintage_count = 0

        for row in cursor.execute(query2):
            wine_count = row[0]

        for row in cursor.execute(query1):
            vintage_count = row[0]

        data.append([country, wine_count, vintage_count, wine_count + vintage_count])

    df = pd.DataFrame(data, columns=['Country', 'Wine Count', 'Vintage Count', 'Total Count'])

    countries = df['Country']
    wine_counts = df['Wine Count']
    vintage_counts = df['Vintage Count']
    total_counts = df['Total Count']

    plt.figure(figsize=(10, 6))
    plt.bar(countries, wine_counts, label='Wine Count')
    plt.bar(countries, vintage_counts, bottom=wine_counts, label='Vintage Count')
    plt.bar(countries, total_counts, bottom=[i+j for i,j in zip(wine_counts, vintage_counts)], label='Total Count')

    plt.xlabel('Country')
    plt.ylabel('Count')
    plt.title('Breakdown of Counts by Country')

    plt.legend()
    plt.xticks(rotation=90)
    st.pyplot(plt)

    low_count_500 = st.button('click to see 0-500 counts specifically')
    low_count_100 = st.button('click to see 0-100 counts specifically')
    low_count_20 = st.button('click to see 0-20 counts specifically')

    if low_count_500:
        plt.ylim(0, 500)
        st.pyplot(plt)
    elif low_count_100:
        plt.ylim(0,100)
        st.pyplot(plt)
    elif low_count_20:
        plt.ylim(0,20)
        st.pyplot(plt)
  
def ratings_of_top15wines():
    q1 = '''SELECT name , ratings_average
       FROM Cabernet_Sauvignon
       ORDER BY ratings_average DESC
       LIMIT 5'''
    q2 = '''SELECT name , ratings_average
        FROM Chardonnay
        ORDER BY ratings_average DESC
        LIMIT 5'''
    q3 = '''SELECT name , ratings_average
        FROM Pinot_Noir
        ORDER BY ratings_average DESC
        LIMIT 5'''

    queries = [q1, q2, q3]
    grape_names = ['Cabernet Sauvignon', 'Chardonnay', 'Pinot Noir']

    dataframes = []

    for i, query in enumerate(queries):
        results = cursor.execute(query).fetchall()
        df = pd.DataFrame(results, columns=['Wine Name', 'Ratings Average'])
        df['Grape'] = grape_names[i]
        dataframes.append(df)

    # Combine the DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    sns.barplot(data=combined_df, x='Wine Name', y='Ratings Average', hue='Grape')
    plt.xlabel('Wine Name')
    plt.ylabel('Ratings Average')
    plt.title('Top Rated Wines by Grape')
    plt.xticks(rotation=90)
    st.pyplot(plt)

    rating_4_5 = st.button('click to see ratings from 4 to 5 specifically')

    if rating_4_5:
        plt.ylim(4, 5)
        st.pyplot(plt)

sidebar = st.sidebar.radio('Select one of the options to view :', ["Contents","Oleksandr", "Sam H", "Mythili"])

if sidebar == "Contents":
    st.subheader("welcome to project Vivino")


if sidebar == "Mythili":
    choice = st.selectbox('Choose one to visualise',['Usage of top 5 grapes accross countries',
                                                    'Wines, Vintage and total wines count of each countries',
                                                    'Ratings of top 15 wines of top 3 grapes'])

    if choice == 'Usage of top 5 grapes accross countries':
        heatmap_for_grape()
    elif choice == 'Wines, Vintage and total wines count of each countries':
        barchart_for_countries_WinesVintageCount()
    elif choice == 'Ratings of top 15 wines of top 3 grapes':
        ratings_of_top15wines()

# closing database
cursor.close()
connection.close()
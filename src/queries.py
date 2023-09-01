import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator
import streamlit.components.v1 as components

def heatmap_for_grape(cursor):
    st.header('Top 5 grapes accross countries')

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

def ratings_of_top15wines(cursor):
    # question 6 - second part - ratings of top 15 wines (of top 3 grapes each)
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

def barchart_for_countries_WinesVintageCount(cursor):
    # not from questions - new findings
    st.header('Wines and Vintage count of each countries')

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

        data.append([country, wine_count, vintage_count])

    df = pd.DataFrame(data, columns=['Country', 'Wine Count', 'Vintage Count'])

    countries = df['Country']
    wine_counts = df['Wine Count']
    vintage_counts = df['Vintage Count']

    plt.figure(figsize=(10, 6))
    plt.bar(countries, wine_counts, label='Wine Count')
    plt.bar(countries, vintage_counts, bottom=wine_counts, label='Vintage Count')

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

def marketing_budget(engine):
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
    df1 = pd.read_sql((question2query1), engine)
    df2 = pd.read_sql((question2query2), engine)
    df3 = pd.read_sql((question2query3), engine)
    df4 = pd.read_sql((question2query4), engine)

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
    
    st.pyplot(fig1.figure)

def wine_flavor(engine):
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

    df5 = pd.read_sql((question4query2), engine)
    df6 = pd.read_sql((question4query1), engine)

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

def top_ten_wines(w, h):
    st.markdown(
    """
        <style>
            .block-container {
            max-width: 100%;
            }
            .css-1y4p8pa {
            padding: 0
        </style>
    """,
        unsafe_allow_html=True,
    )
    slide = "<div class='tableauPlaceholder' id='viz1693476912469' style='position: relative'><noscript><a href='#'><img alt='10 wines to increase our sales ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;Top10Winestoincreaseoursales&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Top10Winestoincreaseoursales&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;Top10Winestoincreaseoursales&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1693476912469');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"

    components.html(
        slide, width=w, height=h/6
    )

    slide2 = "<div class='tableauPlaceholder' id='viz1693477582213' style='position: relative'><noscript><a href='#'><img alt='Sheet 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ma&#47;Mapfromwhichcoutrysthiswinefromwithaverageprice&#47;Sheet2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Mapfromwhichcoutrysthiswinefromwithaverageprice&#47;Sheet2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ma&#47;Mapfromwhichcoutrysthiswinefromwithaverageprice&#47;Sheet2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1693477582213');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"
    components.html(
        slide2, width=w, height=h/2
    )

def rating_by_country(w, h):
    st.markdown(
    """
        <style>
            .block-container {
            max-width: 100%;
            }
            .css-1y4p8pa {
            padding: 0
        </style>
    """,
        unsafe_allow_html=True,
    )
    slide = "<div class='tableauPlaceholder' id='viz1693484658147' style='position: relative'><noscript><a href='#'><img alt='Average Rating by Country: A Global Perspective ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ma&#47;MapTopByCountry&#47;Sheet2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='MapTopByCountry&#47;Sheet2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ma&#47;MapTopByCountry&#47;Sheet2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1693484658147');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"

    components.html(
        slide, width=w, height=h
    )

def rating_by_year(w, h):
    st.markdown(
    """
        <style>
            .block-container {
            max-width: 100%;
            }
            .css-1y4p8pa {
            padding: 0
        </style>
    """,
        unsafe_allow_html=True,
    )
    slide = "<div class='tableauPlaceholder' id='viz1693484925098' style='position: relative'><noscript><a href='#'><img alt='Rating by Vintages Year ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ra&#47;RatingByVintagesYear&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='RatingByVintagesYear&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ra&#47;RatingByVintagesYear&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1693484925098');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"

    components.html(
        slide, width=w, height=h
    )

def vip(w, h):
    st.markdown("""
        <style>
                .block-container {
                    max-width: 100%;
                }
                .css-1y4p8pa {
                    padding: 0
                }
                .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 0rem;
                    padding-right: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                }
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
    
    slide = "<div class='tableauPlaceholder' id='viz1693485024241'style='position: relative'><noscript><a href='#'><img alt='Top 5 Wines for VIP client  that have &quot;Cabernet Sauvignon&quot; in their names ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bu&#47;Buble_16934768498600&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Buble_16934768498600&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bu&#47;Buble_16934768498600&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1693485024241');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"

    components.html(
        slide, width=w, height=h
    )

def end():
    st.write('# Thank you for your time')
    value = st.slider('How much do you like wine', 0, 100)
    if value <= 25:
        like = st.button('I do not like wine')
        dont_drink = st.button('I do not drink wine')
        if like:
            st.write("That's interesting!")
        elif dont_drink:
            st.write("I appretiate your honesty")
    elif value > 25 and value <= 75:
        occasion = st.button('I drink wine occationaly')
        if occasion:
            st.write('Good for you!')
    elif value > 75:
        always = ("I drink wine on daily basis")
        if always:
            st.write("Go wine! Go wild!")
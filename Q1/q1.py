import sqlite3
import csv

# Modified query to use LEFT JOIN with the wineries table
top_wines_query = """
SELECT 
    wines.name AS wine_name, 
    COALESCE(wineries.name, 'Unknown') AS winery_name, 
    regions.name AS region_name, 
    countries.name AS country_name, 
    vintages.year AS vintage_year,
    AVG(vintages.ratings_average) AS average_rating,
    SUM(vintages.ratings_count) AS total_number_of_ratings,
    AVG(vintages.price_euros) AS average_price
FROM 
    wines
LEFT JOIN 
    wineries ON wines.winery_id = wineries.id
JOIN 
    regions ON wines.region_id = regions.id
JOIN 
    countries ON regions.country_code = countries.code
JOIN 
    vintages ON wines.id = vintages.wine_id
WHERE 
    vintages.price_euros IS NOT NULL
GROUP BY 
    wine_name, winery_name, region_name, country_name, vintage_year
HAVING 
    total_number_of_ratings > 30
ORDER BY 
    average_rating DESC, 
    total_number_of_ratings DESC, 
    average_price ASC
LIMIT 10;
"""

# Connect to the database
conn = sqlite3.connect('data/vivino.db')
cursor = conn.cursor()

# Execute the modified query
cursor.execute(top_wines_query)
left_join_top_10_wines_results = cursor.fetchall()

# Save results to a CSV file
csv_file_path = 'data/top_10_wines_modified_full.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(["Wine Name", "Winery", "Region", "Country", "Vintage Year", "Average Rating", "Number of Ratings", "Price (Euros)"])
    # Write data
    writer.writerows(left_join_top_10_wines_results)

# Close the database connection
conn.close()

csv_file_path

# We'll compile the steps taken into a single code block and save the result into a CSV file.
import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('data/vivino.db')
cursor = conn.cursor()

# Step 1: Identify wines with "Cabernet Sauvignon" in their names
query_wines = """
SELECT 
    id, name 
FROM 
    wines 
WHERE
    name LIKE '%Cabernet Sauvignon%'
"""
cab_sauvignon_wines = cursor.execute(query_wines).fetchall()
cab_sauvignon_wine_ids = [wine[0] for wine in cab_sauvignon_wines]

# Step 2: Extract the top 5 vintages for the identified Cabernet Sauvignon wines
query_top_vintages = f"""
SELECT 
    vintages.name, 
    vintages.ratings_average, 
    vintages.ratings_count, 
    wines.name 
FROM 
    vintages 
JOIN 
    wines ON vintages.wine_id = wines.id
WHERE 
    vintages.wine_id IN ({','.join(map(str, cab_sauvignon_wine_ids))})
ORDER BY 
    vintages.ratings_average DESC,
    vintages.ratings_count DESC
LIMIT 5
"""
top_cab_sauvignon_vintages = cursor.execute(query_top_vintages).fetchall()

# Close the connection
conn.close()

# Save the result to a CSV file
csv_filename = "data/top_vip_sauvignon_vintages.csv"
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Vintage Name', 'Average Rating', 'Number of Ratings', 'Wine Name'])
    writer.writerows(top_cab_sauvignon_vintages)

csv_filename

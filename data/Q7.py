import sqlite3
import csv

# Connect to the database
conn = sqlite3.connect('data/vivino.db')
cursor = conn.cursor()

# SQL query to calculate average wine rating for each country
avg_rating_per_country_query = """
SELECT 
    c.name AS country_name, 
    AVG(w.ratings_average) AS average_rating
FROM 
    wines w
JOIN 
    regions r ON w.region_id = r.id
JOIN 
    countries c ON r.country_code = c.code
GROUP 
    BY c.name
ORDER 
    BY average_rating DESC;
"""
avg_rating_per_country = cursor.execute(avg_rating_per_country_query).fetchall()

# SQL query to calculate average rating for each vintage
avg_rating_per_vintage_query = """
SELECT 
    v.year AS vintage_year, AVG(v.ratings_average) AS average_rating
FROM 
    vintages v
GROUP 
    BY v.year
ORDER 
    BY average_rating DESC;
"""
avg_rating_per_vintage = cursor.execute(avg_rating_per_vintage_query).fetchall()

# Function to save the results to a CSV file
def save_to_csv(data, headers, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        
        # Iterate through the rows and round the 'Average Rating' before writing to CSV
        for row in data:
            csvwriter.writerow([row[0], round(float(row[1]), 1)])

# Save average wine rating for each country to CSV
country_filename = "data/average_rating_by_country.csv"
country_headers = ["Country", "Average Rating"]
save_to_csv(avg_rating_per_country, country_headers, country_filename)

# Save average rating for each vintage to CSV
vintage_filename = "data/average_rating_by_vintage.csv"
vintage_headers = ["Vintage Year", "Average Rating"]
save_to_csv(avg_rating_per_vintage, vintage_headers, vintage_filename)

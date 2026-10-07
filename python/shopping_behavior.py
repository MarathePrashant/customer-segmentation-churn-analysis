import pandas as pd
import numpy as np

df= pd.read_csv(r"C:\Users\prash\OneDrive\Documents\PERSONAL LIBRARY\Programming\GitHub\customer_shopping_behavior\customer_shopping_behavior.csv")
print("First Five Rows :")
print(df.head())
print("Last Five Rows :")
print(df.tail())

##More insight of Data 
print(df.info())

##Statistical Summary of numerical coloms
description = df.describe(include="all")
print(description)

##Missing Values
missing_values = df.isnull().sum()
print(missing_values)

df["Review Rating"] = df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))
print(df.isnull().sum())

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(" ","_")
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)

###Feature Engineering

##Creating_New_Columns
labels = ["Young_Adult","Adult","Middle_Age","Senior"]
df["age_group"] = pd.qcut(df['age'],q=4,labels=labels)

print(df[['age','age_group']].head(10))

##Purchase Frequency
Frequeny_map = {
    'Forenighgt':14,
    'Weekly':7,
    'Monthly':30,
    'Quaterly':90,
    'Bi-Weekly':14,
    'Annually':365,
    'Every_three_months':90
}

df['purchases_frequency_days'] = df['frequency_of_purchases']
print(df[['purchases_frequency_days','frequency_of_purchases']].head(10)) 

print(df[['discount_applied','promo_code_used']].head(30))

print((df['discount_applied'] == df['promo_code_used']).all())
df = df.drop('promo_code_used',axis=1)

print(df.columns)

##Save the cleaned dataset as a new CSV file
output_path = r"C:\Users\prash\OneDrive\Documents\PERSONAL LIBRARY\Programming\GitHub\customer_shopping_behavior\customer_shopping_behavior_cleaned.csv"
df.to_csv(output_path, index=False)

print("Cleaned dataset saved successfully!")
print(f"File location: {output_path}")

##Connecting to PostgreSQL
import pandas as pd
from sqlalchemy import create_engine

# Connecting to PostgreSQL
username = "postgres"
password = "**********"
host = "-----------"
port = "5432"
database = "shopping_behavior"

engine = create_engine(
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

table_name = "customer_behaviour"

df.to_sql(table_name,engine,if_exists="replace",index=False)

print(f"Data successfully loaded into table "
    f"'{table_name}' in database '{database}'.")

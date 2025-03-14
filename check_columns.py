import pandas as pd

# Load dataset
df = pd.read_csv("dummy_npi_data.csv")

# Print all column names
print("Columns in dataset:", df.columns.tolist())

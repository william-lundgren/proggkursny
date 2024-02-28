import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'ASan Francisco', 'Los Angeles']
})

# Creating multiple conditions
condition1 = (df['Age'] > 25)
condition2 = (df['City'] != 'New York')
condition3 = (df['Name'].str.startswith('A'))

# Combining conditions using logical operators
combined_condition = condition1 & condition2 & condition3

# Using loc with multiple conditions
result_df = df.loc[combined_condition]

# Display the result
print(result_df)
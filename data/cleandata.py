import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = 'C:\\Users\\ASUS\\Desktop\\241-152\\finalproject\\air4thai44t2023-01-012024-02-27.csv'
data = pd.read_csv(file_path)


# Drop columns with more than 50% NaN values
data.dropna(axis=1, thresh=1, inplace=True)

data['O3'].fillna(data['O3'].mean(), inplace=True)
data['PM25'].fillna(data['PM25'].mean(), inplace=True)



# Handle zeros separately
columns_to_handle_zeros = ['PM25', 'O3', 'WS', 'TEMP', 'RH', 'WD']


new_data = data.drop(index=range(1392, len(data)))
cleaned_file_path = 'C:\\Users\\ASUS\\Desktop\\241-152\\finalproject\\data\\new_cleaned_data.csv'
new_data.to_csv(cleaned_file_path, index=False)

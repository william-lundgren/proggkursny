import pandas as pd
import matplotlib.pyplot as plt
import math
# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 1
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
# Create pandas dataframe objects from csv files, make sure to specify separator charactor to properly read the csv
df_cpi = pd.read_csv("cpi.csv", sep=";")
df_regions = pd.read_csv("regions.csv", sep=";")
df_inflation = pd.read_csv("inflation.csv")

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 2
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

# Make it a function to make code more readable
def get_country_code(country_name):
    # make the country names lowercase since spaces mess up the capitalize check
    # get all the column values where the land column matches the name
    return df_regions[df_regions['Land'].str.lower() == country_name.lower()]['Landskod'].values[0]

def get_country_name(country_code):
    # make the country names lowercase since spaces mess up the capitalize check
    # get all the column values where the landskod column matches the code
    return df_regions.loc[df_regions["Landskod"].str.lower() == country_code.lower(), "Land"].values[0]

def get_country_names(country_codes):
    names = []
    for code in country_codes:
        # make the country names lowercase since spaces mess up the capitalize check
        # get all columns that have matching values with country code and add to names
        names.append(df_regions.loc[df_regions["Landskod"].str.lower() == code.lower(), "Land"].values[0])
    return names

def get_inflation_by_year(year):
    return df_cpi[["Landskod", year]]


def get_inflation_by_country_code(code):
    # more clean way to get the country code consistently
    # matches the landkod column in dfcpi which values that are equal to the code
    return df_cpi[df_cpi['Landskod'].str.lower() == code.lower()].iloc[0]


def sanitize_input(x, y):
    # give a dataframe y and list x of values to plot containing nan, will return both list with values removed
    # accordingly
    # if x==none means we just want to sanitize the output set and not the matching input

    # Sanitize input and remove the nan from the dataframe
    to_remove = []

    # add to a different array so we dont remove while iterating, gives more readable code
    for j, entry in enumerate(y.values.tolist()[1:]):
        if math.isnan(entry) or math.isinf(entry):
            print(entry, "is nan")
            to_remove.append(j)

    for index in to_remove:
        # index will correspond to offset from start year, so we can add 1960 with index to get which value to remove
        # for both year list and inflation data
        y = y.drop(str(1960 + index))
        x.remove(1960 + index)

    # if we dont care about x (is none) return only y since it was the only one we modified and used
    return x, y if x is not None else y


# ---- PART A: ----

countries = []


while True:
    # we assume we get proper inputs, since input handling is tedious and not the point of this exercise
    user_input = input("Enter the countries to be included in analysis (max 3). End your input with END: ")
    if user_input.upper() == "END":  # auto make it upper so it doesn't break with improper capitalization
        break
    # Auto capitalize so it doesnt break with improper capitalization
    countries.append(user_input.capitalize())

country_codes = []

for country_name in countries:
    # Convert input country names to country codes so we can find in the dataframe
    country_codes.append(get_country_code(country_name))

# Create figure for the 1-3 countries with proper size
plt.figure(figsize=(10, 6))
# Enumerate so we can get the index of the list and get correspoding value in the country name list for the legend
for i, country_code in enumerate(country_codes):
    years = list(range(1960, 2023))
    inflation = get_inflation_by_country_code(country_code)

    years, inflation = sanitize_input(years, inflation)

    # make inflation into a list and remove the leading country code in the list so we can use it to plot
    inflation = inflation.values.tolist()[1:]

    # get the max and min value along with according year to mark in plot
    max_value = max(inflation)
    max_year = years[inflation.index(max_value)]

    min_value = min(inflation)
    min_year = years[inflation.index(min_value)]

    # make plot for the min and max values, zorder to make sure it is at the front
    plt.scatter(max_year, max_value, color='red', zorder=10)
    plt.scatter(min_year, min_value, color='blue', zorder=10)

    # to make sure the plot follows the specified parameters with title labels and grid as well as vertical ticks
    plt.plot(years, inflation, label=countries[i])
    plt.title("Inflation under tidsperioden 1960-2022")
    plt.xlabel("År")
    plt.ylabel("inflationstalet [%]")
    plt.grid(True)
    plt.xticks(years, rotation='vertical')
    plt.legend()
plt.show()

# ---- PART B: ----


def FF(curr_inflation, last_inflation):
    # input the inflation as a list, years as a list and year is the year to get a value for
    return (curr_inflation - last_inflation) / last_inflation

# Figure with proper size
plt.figure(figsize=(10, 6))
# we assume we get proper inputs, since input handling is tedious and not the point of this exercise

country_name = input("Enter name of country to analyse change in inflations for: ")

country_code = get_country_code(country_name.capitalize())

years = list(range(1960, 2023))
inflation = get_inflation_by_country_code(country_code)
years, inflation = sanitize_input(years, inflation)

# make inflation into a list and remove the leading country code in the list so we can use it to plot
inflation = inflation.values.tolist()[1:]

change_inflation = []
for index, value in enumerate(inflation[1:]):
    change_inflation.append(FF(value, inflation[index]))

# add the 0th element
change_inflation.insert(0, 0)

# to make sure the plot follows the specified parameters with title labels and grid as well as vertical ticks
plt.bar(years, change_inflation)
plt.title(f"{country_name.capitalize()} - förändring av inflationen i förhållande till föregående år (1960-2022)")
plt.xlabel("År")
plt.ylabel("Förändring [%]")
plt.grid(True)
plt.xticks(years, rotation='vertical')
plt.show()

# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 3
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

def print_table(top, bottom, year):
    # Print all the lines for the table
    length = 70
    # set the length that is used for multiple places for the horizontal lines

    print("=" * length)
    print("L ä n d e r   m e d   h ö g s t   o c h   l ä g s t   i n f l a t i o n ")
    # make the text centered
    print(f" Å R   {year}".center(length, " "))
    print("-" * length)
    print("Lägst".center(int(length/2), " ") + "Högst".center(int(length/2), " "))
    # played around with the spacing and this made it look good
    print("Land" + " " * 15 + "inflation [%]" + " " * 4 + "Land" + " " * 15 + "inflation [%]")
    print("-"*length)

    # 6 countries to print
    for i in range(6):
        # since the input is a list of tuples this is how we access the data. ljust makes it so it fills with spaces
        # to accommodate different length country names
        first = str(bottom[i][0]).ljust(25) + str(bottom[i][1])
        second = str(top[i][0]).ljust(25) + str(top[i][1])
        print(first + " " * 7 + second)

    print("="*length)

# we assume we get proper inputs, since input handling is tedious and not the point of this exercise
year = input("Ange årtal som ska analyseras: ")

inflation = get_inflation_by_year(year)

# figure with proper size
plt.figure(figsize=(10, 6))

# Sanitize input and remove the nan from the dataframe
to_remove = []

# add to a different array so we dont remove while iterating, gives more readable code
for i, entry in enumerate(inflation.values.tolist()):
    if math.isnan(entry[1]) or math.isinf(entry[1]):
        to_remove.append(i)

for index in to_remove:
    # index will correspond to offset from start year, so we can add 1960 with index to get which value to remove
    # for both year list and inflation data
    inflation = inflation.drop(index)

# Get the bottom 6
sorted_df = inflation.sort_values(by=f"{year}")
country_codes = sorted_df["Landskod"].tolist()
inflations = sorted_df[f"{year}"].tolist()

# change data into format we want for the print function and only use the first 6 since we are plotting
# bottom and top 6 only
bottom = list(zip(country_codes, inflations))[:6]

# Get the names and values for the bottom countries for the bar plot
names_1 = get_country_names(country_codes[:6])
values_1 = inflations[:6]

# Get the top 6
sorted_df = inflation.sort_values(by=f"{year}", ascending=False)

country_codes = sorted_df["Landskod"].tolist()
inflations = sorted_df[f"{year}"].tolist()

# in order to get it to the format that the print table function wants
top = list(zip(country_codes, inflations))[:6]

# Get the names and values for the bottom countries for the bar plot
names_2 = list(reversed(get_country_names(country_codes[:6])))
values_2 = list(reversed(inflations[:6]))

# combine the data of the top and bottom to give the complete wanted data
bar_names = names_1 + names_2
bar_values = values_1 + values_2

# Create the plot
plt.bar(bar_names, bar_values)
plt.title(f"De lägsta och högsta inflationerna uppmätta år {year}")
plt.grid(True)
plt.xticks(rotation=20)
plt.show()

# The data is still using country codes since the regions set for some reason is not the complete set of country code
# to names, (AFW is missing for example) so we convert it here when we use it instead. a bit messier

bottom_with_names = []
top_with_names = []

# Since we only want short form on the data we need to round it
# Create the new data using the country code to get the name and round the number and append to list
# Then use it to print the data.
# The data is a list of tuples where [(country1, inflation1), (country2, inflation2), ...]
for country_set in bottom:
    new_data = (get_country_name(country_set[0]), str(round(country_set[1], 1)))
    bottom_with_names.append(new_data)

for country_set in top:
    new_data = (get_country_name(country_set[0]), str(round(country_set[1], 1)))
    top_with_names.append(new_data)

print_table(top_with_names, bottom_with_names, year)


# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
def analyze_inflation_by_continent(df_cpi, df_regions):
    merged_df = pd.merge(df_cpi, df_regions[['Landskod', 'Kontinent']], how='left', on='Landskod')

    # Converts 1960 to 2022 to ints
    merged_df.loc[:, '1960':'2022'] = merged_df.loc[:,'1960':'2022'].apply(pd.to_numeric, errors='coerce')

    # Highest inflation per continent
    max_inflation = merged_df.groupby('Kontinent').max()

    # Lowest inflation per continent
    min_inflation = merged_df.groupby('Kontinent').min()

    return max_inflation, min_inflation


def print_table(avg_inflation, max_inflation, min_inflation):
    # Format table
    print("="*80)
    print("O L I K A  K O N T I N E N T E R S  I N F L A T I O N  U N D E R")
    print("T I D S P E R I O D E N  1 9 6 0 -- 2 0 2 2")
    print("-"*80)
    print(f"{'Högst':<10}{'Lägst':<10}{'Medel 1960-2022':<10}")
    print("-"*80)

    # Loop through the averages
    for continent, inflation in avg_inflation.items():
        highest_country = max_inflation.loc[continent, 'Landskod']
        highest_inflation = max_inflation.loc[continent, '2022']
        lowest_country = min_inflation.loc[continent, 'Landskod']
        lowest_inflation = min_inflation.loc[continent, '1960']
        mean_inflation = data.mean()
        print(f"{continent:<10}{highest_country} {highest_inflation:<10.1f} {lowest_country} {lowest_inflation:<10.1f}{mean_inflation:<10.1f}")

years = range(1960, 2023)

merged_df = pd.merge(df_cpi, df_regions, left_on="Landskod", right_on="Landskod")

# All the continents in the table, quick check can be done by getting the continents column as a list and convert to a set
# could of course leave it like that but this is more readable and works since there arent so many distinct values
continents = ["Africa", "Oceania", "Europe", "America", "Asia"]

averages = {}
for continent in continents:
    # Calculate the averages per continent
    cont_avg = 0
    count = 0
    data = merged_df.loc[merged_df["Kontinent"] == continent]

    for year in years:
        # value counts removes all the nan and index gets the actual values, quick and easy way to get the average
        # since we dont want the number of NaN to go into our average
        values = data[str(year)].value_counts().index.tolist()
        cont_avg += sum(values)
        count += len(values)

    infl_average = cont_avg / count
    averages[continent] = infl_average

max_inflation, min_inflation = analyze_inflation_by_continent(df_cpi, df_regions)


# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:
def get_5_min(df):
    # we can easily get the min by sorting the dataframe by ascending and get the 5 first elements
    df = df.sort_values("Value", ascending=True)[:5]
    # then extract the years and inflation for those values.
    years = df["TIME"]
    inflations = df["Value"]

    # Make sure they years are ints so they plot properly
    years = [int(year) for year in years.tolist()]

    return years, inflations.tolist()


def get_5_max(df):
    # we can easily get the max by sorting the dataframe by descending and get the 5 first elements
    df = df.sort_values("Value", ascending=False)[:5]
    # then extract the years and inflation for those values.
    years = df["TIME"]
    inflations = df["Value"]

    # Make sure they years are ints so they plot properly
    years = [int(year) for year in years.tolist()]

    return years, inflations.tolist()

# we assume we get proper inputs, since input handling is tedious and not the point of this exercise
country = input("Ange vilket land som ska analyseras (ex Sweden): ")
subject = input("Ange vilken subject du vill analysera (FOOD, ENRG, TOT eller TOT_FOODENR): ")
frequency = input("Ange vilken frequency du vill analysera (A, M eller Q): ")
measure = input("Ange vilken measure du vill analysera (AGRWTH, IDX2015): ")

# Merge the databases into one using the location and landskod columns where matching.
# then we can just plot the results
merged_df = pd.merge(df_inflation, df_regions, left_on="LOCATION", right_on="Landskod")

# Set all the conditions based on the input data
condition_1 = (merged_df["Land"] == country.capitalize())
condition_2 = (merged_df["SUBJECT"] == subject.upper())
condition_3 = (merged_df["FREQUENCY"] == frequency.upper())
condition_4 = (merged_df["MEASURE"] == measure.upper())

# Get the rows that match our input data
results = merged_df.loc[condition_1 & condition_2 & condition_3 & condition_4]

# The inflation is in the value column and now we have sorted out all the relevant rows, so what we want to plot
# is fully contained in the value column
years = results["TIME"].tolist()
# convert to int so it gets plotted properly
years = [int(year) for year in years]

y = results["Value"]

# Get the years and values for the 5 min and max years to make circles
min_years, min_inflation = get_5_min(results)
max_years, max_inflation = get_5_max(results)

# Since they are lists and properly ordered we can just loop through them both at the same time and plot their respective values
for i, year in enumerate(min_years):
    plt.scatter(year, min_inflation[i], label=f"{year}, Minsta")

for i, year in enumerate(max_years):
    plt.scatter(year, max_inflation[i], label=f"{year}, Högsta")

# Do all the plotting so it fits the specifications
plt.plot(years, y)
plt.xticks(years, rotation=60)
plt.grid(True)
plt.xlabel("År")
plt.ylabel("Inflation")
plt.title(f"Inflation för {country.capitalize()}, {subject.upper()}, {frequency.upper()} och {measure.upper()}")
plt.legend()
plt.show()


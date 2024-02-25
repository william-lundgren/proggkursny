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
    return df_regions[df_regions['Land'] == country_name]['Landskod'].values[0]


def get_inflation_by_country_code(code):
    return df_cpi[df_cpi['Landskod'] == code].iloc[0]
#    return df_cpi[df_cpi['Landskod'] == code].iloc[0].values.tolist()[1:]

def sanitize_input(x, y):
    # give a dataframe y and list x of values to plot containing nan, will return both list with values removed
    # accordingly

    # Sanitize input and remove the nan from the dataframe
    to_remove = []

    # add to a different array so we dont remove while iterating, gives more readable code
    for j, entry in enumerate(y.values.tolist()[1:]):
        if math.isnan(entry) or math.isinf(entry):
            to_remove.append(j)

    for index in to_remove:
        # index will correspond to offset from start year, so we can add 1960 with index to get which value to remove
        # for both year list and inflation data
        y = y.drop(str(1960 + index))
        x.remove(1960 + index)

    return x, y


# ---- PART A: ----

countries = []


while True:
    user_input = input("Enter the countries to be included in analysis (max 3). End your input with END: ")
    if user_input.upper() == "END":  # auto make it upper so it doesn't break with improper capitalization
        break
    # Auto capitalize so it doesnt break with improper capitalization
    countries.append(user_input.capitalize())

country_codes = []

for country_name in countries:
    # Convert input country names to country codes so we can find in the dataframe
    country_codes.append(get_country_code(country_name))

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


# ---- PART B: ----


def FF(curr_inflation, last_inflation):
    # input the inflation as a list, years as a list and year is the year to get a value for
    print(curr_inflation, last_inflation)
    return (curr_inflation - last_inflation) / last_inflation


plt.figure()
country_name = input("Enter name of country to analyse change in inflations for: ")

country_code = get_country_code(country_name.capitalize())

years = list(range(1960, 2023))
inflation = get_inflation_by_country_code(country_code)
years, inflation = sanitize_input(years, inflation)

# make inflation into a list and remove the leading country code in the list so we can use it to plot
inflation = inflation.values.tolist()[1:]

change_inflation = []
print(inflation)
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




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 4
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:

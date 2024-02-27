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

def get_country_name(country_code):
    return df_regions.loc[df_regions["Landskod"] == country_code, "Land"].values[0]

def get_country_names(country_codes):
    names = []
    for code in country_codes:
        names.append(df_regions.loc[df_regions["Landskod"] == code, "Land"].values[0])
    return names

def get_inflation_by_year(year):
    return df_cpi[["Landskod", year]]


def get_inflation_by_country_code(code):
    return df_cpi[df_cpi['Landskod'] == code].iloc[0]


#    return df_cpi[df_cpi['Landskod'] == code].iloc[0].values.tolist()[1:]

def sanitize_input(x, y):
    # give a dataframe y and list x of values to plot containing nan, will return both list with values removed
    # accordingly
    # if x==none means we just want to sanitize the output set and not the matching input

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

    # if we dont care about x (is none) return only y since it was the only one we modified and used
    return x, y if x is not None else y

def uppgift_2():

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

def uppgift_3():

    year = input("Ange årtal som ska analyseras: ")

    inflation = get_inflation_by_year(year)

    # Sanitize input and remove the nan from the dataframe
    to_remove = []

    # add to a different array so we dont remove while iterating, gives more readable code
    for i, entry in enumerate(inflation.values.tolist()):
        if math.isnan(entry[1]) or math.isinf(entry[1]):
            to_remove.append(i)
    #print(inflation)
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
    plt.xticks(rotation=15)
    plt.show()

    # THe data is still using country codes since the regions set for some reason is not the complete set of country code
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




# ------------------------------------------------------------------------------------------------------------------------
# Uppgift 5
# ------------------------------------------------------------------------------------------------------------------------
# Skriv din kod här:


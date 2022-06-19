import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'newyork': 'new_york_city.csv',
            #   'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
availableMonths = ["january", "february", "march", "april", "may", "june"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    cities = ["chicago", "newyork", "washington"]
    filters = ["month", "day", "both", "none"]
    

    reqCityMsg = "Would you like to see data for Chicago, New York or Washington?\n"
    reqFilterMsg = 'Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter\n'
    reqMonthMsg = 'Which month - January, February, March, April, May, or June?\n'
    reqDayMsg = 'Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n'
    city = fltr = ""
    month = day = "all"
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        # city = input("Please enter the city you are looking for? (Chicago, New York, Washington)\n")
        city = input(reqCityMsg)
        city = city.replace(" ", "").lower()
        if city not in cities:
            reqCityMsg = "There is no data for this city. Please enter one of those cities? (chicago, new york, washington)\n"
        else:
            break
    # Filter 
    while True:
        fltr = input(reqFilterMsg)
        fltr = fltr.replace(" ", "").lower()
        if fltr not in filters:
            print("Invalid Input")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        if fltr in ["month", "both"]:
            month = input(reqMonthMsg)
            month = month.replace(" ", "").lower()
            if month not in availableMonths:
                print("Invalid Input")
            else:
                break
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        if fltr in ["day", "both"]:
            day = input(reqDayMsg)
            day = day.replace(" ", "").lower()
            if day not in days:
                print("Invalid Input")
            else:
                break
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """ 
    df = pd.read_csv(CITY_DATA[city])
    if month != "all":
        monthIndx = availableMonths.index(month)+1
        df = df[pd.to_datetime(df['Start Time']).dt.month == monthIndx]
    if day != "all":
        df = df[pd.to_datetime(df['Start Time']).dt.day_name() == day.capitalize()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    dfTmp = df.copy()
    try:
        # display the most common month
        dfTmp['month'] = pd.to_datetime(df['Start Time']).dt.month
        popular_month = availableMonths[dfTmp['month'].mode()[0]-1]
        print("Most popular Month: {}".format(popular_month))


        # display the most common day of week
        dfTmp['day'] = pd.to_datetime(df['Start Time']).dt.day_name()
        popular_day = dfTmp['day'].mode()[0]
        print("Most popular day: {}".format(popular_day))

        # display the most common start hour
        dfTmp['hour'] = pd.to_datetime(df['Start Time']).dt.hour
        popular_hour = dfTmp['hour'].mode()[0]
        print("Most popular hour: {}".format(popular_hour))
    except:
        print("Something Went Wrong")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
        # display most commonly used start station
        popular_startStation = df['Start Station'].mode()[0]
        print("Most commonly used start station: {}".format(popular_startStation))

        # display most commonly used end station
        popular_endStation = df['End Station'].mode()[0]
        print("Most commonly used end station: {}".format(popular_endStation))

        # display most frequent combination of start station and end station trip
        popular_startEndStation = (df['Start Station']+ " ,End station: " +df['End Station']).mode()[0]
        print("Most frequent combination of start station and end station: [Start station: {}]".format(popular_startEndStation))
    except:
        print("Something Went Wrong")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        # display total travel time
        total_travel_time = (pd.to_datetime(df['End Time'])-pd.to_datetime(df['Start Time'])).sum()
        total_travel_time = pd.Timedelta(total_travel_time).total_seconds()
        print("Total travel time: {}".format(total_travel_time))


        # display mean travel time
        mean_travel_time = (pd.to_datetime(df['End Time'])-pd.to_datetime(df['Start Time'])).mean()
        mean_travel_time = pd.Timedelta(mean_travel_time).total_seconds()
        print("Mean travel time: {}".format(mean_travel_time))
    except:
        print("Something Went Wrong")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        user_types = dict(df.groupby('User Type').size())
        print("Counts of user types")
        for t, c in user_types.items():
            print(t+": ",c)

        # Display counts of gender
        if 'Birth Year' in df:
            gender = dict(df.groupby('Gender').size())
            print("\nCounts of gender")
            for t, c in gender.items():
                print(t+": ",c)

        # Display earliest, most recent, and most common year of birth
            oldest = df['Birth Year'].min()
            youngest = df['Birth Year'].max()
            most_common_year = df['Birth Year'].mode()[0]
            print("\nOldest: {}, Youngest: {}, Most common year of birth: {}".format(oldest, youngest, most_common_year))
    except:
        print("Something Went Wrong")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        usr_ans = input("Would like want to see the raw data? Type 'yes' or 'no'.\n")
        try:
            if usr_ans.lower() == "yes":
                startIndx = 0
                endIndx = 5
                nRaws = df.shape[0]
                if endIndx < nRaws:
                    print(df.iloc[startIndx:endIndx])
                else:
                    print(df.iloc[startIndx:])
                while True:
                    usr_ans = input("Would like to see 5 more rows of the data? Type 'yes' or 'no'.\n")
                    startIndx = endIndx
                    endIndx = startIndx + 5
                    if usr_ans.lower() == "yes":
                        if endIndx < nRaws:
                            print(df.iloc[startIndx:endIndx])
                        else:
                            print(df.iloc[startIndx:])
                    else:# usr_ans.lower() == "no":
                        break
        except:
            print("Something Went Wrong")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

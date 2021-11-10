name_of_day
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHLY_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAILY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name = ''
    while city_name.lower() not in CITY_DATA:
        city_name = input("\nWhat is the name of the city to analyze data? (E.g. Input either chicago, new york city, washington)\n")
        if city_name.lower() in CITY_DATA:
            city = CITY_DATA[city_name.lower()]
        else:
            print("Sorry we were not able to get the name of the city to analyze data, Please input either chicago, new york city or washington.\n")

    # user input for month (all, january, february, ... , june)
    month_name = ''
    while month_name.lower() not in MONTHLY_DATA:
        month_name = input("Which month? January, February, March, April, May, or June?")
        if month_name.lower() in MONTHLY_DATA:
            month = month_name.lower()
        else:
            print("Sorry we were not able to get the name of the month to filter data, Please input either 'all' to apply no month filter or january, february, ... , june.\n")

    # user input for day of week (all, monday, tuesday, ... sunday)
    name_of_day = ''
    while name_of_day.lower() not in DAILY_DATA:
        name_of_day = input("\nWhich day?Please type your response as a day of the week(e.g, Sunday\n")
        if name_of_day.lower() in DAILY_DATA:
            day = name_of_day.lower()
        else:
            print("Sorry we were not able to get the name of the day, Please input either 'all' to apply no day filter or monday, tuesday, ... sunday.\n")

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
    # loading data file into a dataframe
    df = pd.read_csv(city)

    # converting the Start Time and End Time into date format yyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekname_of_day
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHLY_DATA.index(month)

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month from the given fitered data is: " + MONTHLY_DATA[common_month].title())

    # Display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week from the given fitered data is: " + common_day_of_week)

    # Display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print("The most common start hour from the given fitered data is: " + str(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station from the given fitered data is: " + common_start_station)

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station from the given fitered data is: " + common_end_station)

    # Display most frequent combination of start station and end station trip
    frequent_combination = (df['Start Station'] + "||" + df['End Station']).mode()[0]
    print("The most frequent combination of start station and end station trip is : " + str(frequent_combination.split("||")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: " + str(total_travel_time))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time in hours is: " + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The number of user types is: \n" + str(user_types))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print("The count of user gender from the given fitered data is: \n" + str(gender))

        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print('The Earliest year of birth is: {}\n'.format(earliest))
        print('Most recent one is: {}\n'.format(most_recent))
        print('and the most common birth one is: {}\n'.format(most_common) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays raw data on user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    print(df.head())
    next = 0
    while True:
        display_data = input('\nWould you like to view more information? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            display_data = input('\nWould you like to view more information? Enter yes or no.\n')
            if display_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

import time
import pandas as pd
import numpy as np


CITY_DATA = ['chicago', 'new york city', 'washington']
CITY_DATA_CSV = { 'chicago': 'chicago.csv', 'new_york_city': 'new_york_city.csv', 'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (Chicago, New York City, Washington).
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?: ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # Get user input for month (all, january, february, ..., june).
    while True:
        month = input("Which month? January, February, March, April, May, June, or all?: ").strip().lower()
        if month in MONTHS:
            break
        else:
            print("Invalid input. Please choose a valid month or 'all'.")

    # Get user input for day of week (all, monday, tuesday, ..., sunday).
    while True:
        day = input("Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?: ").strip().lower()
        if day in DAYS:
            break
        else:
            print("Invalid input. Please choose a valid day of the week or 'all'.")

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
    # Load data file for the specified city
    if city.lower() == CITY_DATA[0]:
        df = pd.read_csv(CITY_DATA_CSV['chicago'])
    elif city.lower() == CITY_DATA[1]:
        df = pd.read_csv(CITY_DATA_CSV['new_york_city'])
    elif city.lower() == CITY_DATA[2]:
        df = pd.read_csv(CITY_DATA_CSV['washington'])
    else:
        raise ValueError("Invalid city name. Please choose from Chicago, New York City, or Washington.")

    # Convert 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from 'Start Time' to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day_of_Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month.lower() != 'all':
        df = df[df['Month'].str.lower() == month.lower()]

    # Filter by day of week if applicable
    if day.lower() != 'all':
        df = df[df['Day_of_Week'].str.lower() == day.lower()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    print("The most common month for travel is:", most_common_month)

    # Display the most common day of week
    most_common_day_of_week = df['Day_of_Week'].mode()[0]
    print("The most common day of the week for travel is:", most_common_day_of_week)

    # Extract hour from 'Start Time' to find the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Hour'].mode()[0]
    print("The most common start hour for travel is:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is:", most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is:", most_common_end_station)

    # Display most frequent combination of start station and end station trip
    most_frequent_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most frequent combination of start station and end station trip is:", most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: {} seconds".format(total_travel_time))

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: {} seconds".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)

    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("\nEarliest year of birth:", int(earliest_birth_year))
        print("Most recent year of birth:", int(most_recent_birth_year))
        print("Most common year of birth:", int(most_common_birth_year))
    else:
        print("\nBirth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(start_index, df):
    """
    Display 5 lines of raw data starting from the specified index.

    Args:
        start_index (int): The starting index of the raw data to display.
    """
    df.iloc[start_index:start_index+5]
    print(df.iloc[start_index:start_index+5])
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)


def main():
    while True:
        city, month, day = get_filters()
        raw_data = load_data(city, month, day)
        
        # Convert raw data to DataFrame
        df = pd.DataFrame(raw_data)
        
        start_index = 0
        while True:
            show_data = input("Do you want to see 5 lines of raw data? (yes/no): ").strip().lower()
            if show_data == 'yes':
                print('='*55)
                display_raw_data(start_index, df)
                start_index += 5
            elif show_data == 'no':
                print('='*55)
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

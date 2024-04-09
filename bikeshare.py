import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    list_city_name = ['chicago', 'new york city', 'washington']
    # Get user input for city (chicago, new york city, washington).
    while True:
        city_input = input("Which city do you want to explore? (chicago, new york city, washington) ").lower()
        if city_input in list_city_name:
            city = city_input
            break
        else:
            print('Invalid city name. Try again')

    # Get user input for month (all, january, february, ... , june)
    while True:
        month_input = input("Which month do you want to explore? (all, january, february, ... , june) ").lower()
        if month_input in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            month= month_input
            break
        else:
            print('Invalid month. Try again')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_of_week_input = input("Which day of week do you want to explore? (all, monday, tuesday, ... sunday) ").lower()
        if day_of_week_input in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            day= day_of_week_input
            break
        else:
            print('Invalid day of week. Try again')

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
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is:", most_common_month)

    # Display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of the week is:", most_common_day_of_week)
    
    # Display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print("The most common start hour is:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is:", most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is:", most_common_end_station)

    # Display most frequent combination of start station and end station trip
    df['Trip Stations'] = df['Start Station'] + ' to ' + df['End Station']
    most_frequent_trip = df['Trip Stations'].mode()[0]

    print("The most frequent combination of start station and end station for a trip is:", most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    df['Trip Duration'] = pd.to_numeric(df['Trip Duration'], errors='coerce')
    total_travel_time_seconds = df['Trip Duration'].sum()

    total_travel_time_hours = total_travel_time_seconds // 3600
    total_travel_time_minutes = (total_travel_time_seconds % 3600) // 60
    print("Total travel time:", total_travel_time_hours, "hours and", total_travel_time_minutes, "minutes")


    # Display mean travel time
    mean_travel_time_seconds = df['Trip Duration'].mean()
    mean_travel_time_minutes = mean_travel_time_seconds // 60
    mean_travel_time_seconds_remaining = mean_travel_time_seconds % 60
    print("Mean travel time:", int(mean_travel_time_minutes), "minutes and", int(mean_travel_time_seconds_remaining), "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()

    print("Counts of user types:")
    for user_type, count in user_type_counts.items():
        print(f"{user_type}: {count}")

    # Display counts of gender
    try: 
        gender_counts = df['Gender'].value_counts()

        print("Counts of gender:")
        for gender, count in gender_counts.items():
            print(f"{gender}: {count}")
    except KeyError:
        print("Gender stat can not be analyze because Gender is not exist in data frame")

    try:
         # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        print("Earliest year of birth:", int(earliest_year_of_birth))

        most_recent_year_of_birth = df['Birth Year'].max()
        print("Most recent year of birth:", int(most_recent_year_of_birth))

        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print("Most common year of birth:", int(most_common_year_of_birth))
    except KeyError:
        print("Birth Year stat can not be analyze because Birth Year is not exist in data frame")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    start_index = 0
    end_index = 5
    while True:
        if start_index == 0:
            answer = input('Would you like to see the 5 lines of raw data? (yes or no) ')
        else:
            answer = input('Would you like to see the next 5 lines of raw data? (yes or no) ')
            
        if answer.lower() == 'yes':
            print(df.iloc[start_index:end_index])
            start_index += 5
            end_index += 5
        elif answer.lower() == 'no':
            break
        else:
            print('Invalid answer. Please enter yes or no')
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

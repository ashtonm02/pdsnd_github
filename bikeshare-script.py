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
    
    print('Hello! Let\'s interrogate some US bikeshare data!')
    
    # Get user input for city.
    while True:
        city = input("Please select a city (chicago, new york city, washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please select from Chicago, New York City or Washington.")
            
    # Get user input for month.
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Please select a month (all, january, february, march, april, may, june): ").strip().lower()
        if month in months:
            break
        else:
            print("Invalid input. Please select a month or select all for all months.")

    # Get user input for day of the week.
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Please select a day (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ").strip().lower()
        if day in days:
            break
        else:
            print("Invalid input. Please select a day or select all for all days of the week.")
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
    
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    try:
        df = pd.read_csv(CITY_DATA[city])

        # Convert the Start Time column to datetime.
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # Extract month and day of the week to create new columns.
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()

        # Filter by month.
        if month != 'all':
            month_name = months.index(month)
            df = df[df['month'] == month_name]

        # Filter by day of the week.
        if day != 'all':
            df = df[df['day_of_week'].str.lower() == day]
        return df
    
    except FileNotFoundError:
        print(f"Error: File '{CITY_DATA[city]}' not found. Please ensure the file exists in the correct location.")
        return None

    
def time_stats(df):
    """
    Displays statistics on the most frequent times of travel
    Args:
        dt(DataFrame): Pandas DataFrame containing bikeshare data
    Returns:
        None
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Display the most common month.
    common_month = df['month'].mode()[0]
    print(f"The most common month is: {common_month}.")

    # Display the most common day of week.
    common_day_of_week = df['day_of_week'].mode()[0]
    print(f"The most common day of the week is: {common_day_of_week}.")

    # Display the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print(f"The most common start hour is: {common_start_hour}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip
    Args:
        df(DataFrame): Pandas DataFrame containing bikeshare data
    Returns:
        None
    """
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}.")

    # Display most commonly used end station.
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}.")

    # Display most frequent combination of start station and end station trip.
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f"The most frequent combination of start and end stations is: {common_trip}.")

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration
    Args:
        df(DataFrame): Pandas DataFrame containing bikeshare data
    Returns:
        None
    """
      
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel_time = np.sum(df['Trip Duration'])
    print(f"Total travel time: {total_travel_time} seconds.")

    # Display mean travel time.
    mean_travel_time = np.mean(df['Trip Duration'])
    print(f"Mean travel time: {mean_travel_time} seconds.") 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users
    Args:
        df(DataFrame): Pandas DataFrame containing bikeshare data
    Returns:
        None
    """   

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_types = df['User Type'].value_counts()
    print("User Types:\n", user_types)

    # Check if 'Gender' column exists in data before displaying counts.
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("\nGender Count:\n", gender_count)
    else:
        print("\nGender data not available for this dataset.")

    # Check if 'Birth Year' column exists in data before displaying statistics.
    if 'Birth Year' in df.columns:
        earliest_birth_year = np.min(df['Birth Year'].dropna())
        print(f"Earliest birth year is: {earliest_birth_year}.")

        recent_birth_year = np.max(df['Birth Year'].dropna())
        print(f"Most recent birth year is: {recent_birth_year}.")

        common_birth_year = df['Birth Year'].mode()[0]
        print(f"Most common birth year is: {common_birth_year}.")
    else:
        print("\nBirth year data not available for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
    Main function to run the US bikeshare data program. This function prompts the user to specifiy a city, month and day of the week to analyse. It loads the data, applies filters based on user selections and displays time, station, trip duration and user statistics. The user can also view 5 lines worth of raw data.
    """
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df is not None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            # Prompt to display raw data.
            start_index = 0
            while True:
                display_raw = input("\nWould you like to see 3 lines of raw data? Enter yes or no.\n")
                if display_raw.lower() != 'yes':
                    break
                print(df.iloc[start_index:start_index+3])
                start_index += 3
                if start_index >= len(df):
                    print("End of data.")
                    break

        else:
            print("Failed to load data. Please check the file path and try again.")

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
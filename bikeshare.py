import time
import pandas as pd
import numpy as np
from datetime import datetime 
from scipy.stats import mode

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

months = ['january', 'february', 'march', 'april', 'may', 'june']

cities = ['washington', 'new york city', 'chicago']

def get_filters():
    """prompt the user for what filters they want to use and return their choices
       Returns city, month, and day to filter on."""
    while True:
        city = str(input('Enter the city you would like data for (or choose all): ')).lower()
        if city in cities or city == 'all':
            break
        else:
            print('Please enter ' + str(cities))
    while True:
        try:
            month = str(input('Choose the month (or all): ')).lower()
            if month in months or month=='all':
                break
        except:
            print('Please enter' + str(months)+ ': ')

    while True:
        try:
            day = str(input('Choose the day of the week (or all): ')).lower()
            if day in days or day == 'all':
                break
            else:
                print('Please enter ' + str(days) + ': ')   
        except:
            print('Please enter ' + str(days) + ': ')               
    return city, month, day

                  




def load_data(city, month_choice, day_choice):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by city, month and day
    """
    df = pd.DataFrame()
    if city != 'all':
        path = CITY_DATA.get(city)
        df = pd.read_csv(path)
        print('Here is the descriptive data for ' + city +'.')
    else:
        for x in range(0,3):
            path = list(CITY_DATA.values())[x]
            city = list(CITY_DATA.keys())[x]
            temp = pd.read_csv(path)
            temp['city'] = city 
            df = df.append(temp, sort=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])  # Ensure it's datetime
    df['End Time'] = pd.to_datetime(df['End Time'])  # Ensure it's datetime

    df['weekday'] = df['Start Time'].dt.strftime("%A").str.lower()
    df['month'] = df['Start Time'].dt.strftime("%B").str.lower()
    
    if month_choice!='all':
        df=df[df['month'] == month_choice]
    if day_choice!='all':
        df=df[df['weekday'] == day_choice]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time=time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')
    hour_tracker = df['Start Time'].dt.hour
    # display the most common month
    print('The most common month is ' + str(df['month'].mode()[0]))

    # display the most common day of week
    print('The most common day of the week is ' + str(df['weekday'].mode()[0]))
    #  display the most common start hour
    print('The most common start hour is ' + str(hour_tracker.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station is ' + str(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('The most common end station is ' + str(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    routes = df['Start Station'] + ' To ' + df['End Station']
    print('The most common trip is ' + str(routes.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Bikeshare customers spent a total of ' + str(sum(df['Trip Duration'])) + ' minutes on bikes.')

    # TO DO: display mean travel time
    print('The average trip was ' + str(sum(df['Trip Duration']) / len(df['Trip Duration']))+ ' minutes.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_counts = df['User Type'].value_counts()
    for user_type, count in user_counts.items():
        print(f'There were {count} {user_type}s that went on trips.')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        for gender, count in genders.items():
            print(f'There were {count} {gender}s that went on trips.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest birth year was ' + str(min(df['Birth Year'])))
        print('The most recent birth year was ' + str(max(df['Birth Year'])))
        print('The most common birth year was ' + str(df['Birth Year'].mode()[0]))
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays the raw data five rows at a time"""
    row_start = 0
    row_end = row_start+5
    while True:
        #Show 5 rows of the data
        if row_end>len(df)-1:
            row_end = len(df)-1
        print(df.iloc[row_start:row_end])
        more = input('Would you like to see more data?')
        if more.lower()!='yes':
            break
        if row_end == len(df)-1:
            break
        row_start+=5
        row_end+=5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data = input('Would you like to see raw data?')
        if raw_data.lower() == 'yes':
            display_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


main()
    

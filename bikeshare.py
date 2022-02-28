# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 10:38:12 2022

@author: a273757
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 15:14:06 2022

@author: David
"""

import time
import pandas as pd
from datetime import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Skrev till MONTHS:
MONTHS = ["January", "February", "March", "April", "May", "June"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filtcer by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Please choose a city: Chicago, Washington or New York City: ").lower()

        print("City", city)
        if city in CITY_DATA:
            print("Thank you! Checking city")
            break
        else:
            print("Please choose a correct city name")
    print("Found city!")

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("What month would you like to check? Write all if you want all months: ").capitalize() 
        print("month", month)
        if month== "All" or month in MONTHS:
            print("Thanks!")
            break
        else:
            print("Not in list, please try again")
    print("ok you choose:", month)
        
    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("What day would you like to check? Write all if you want all days: ").capitalize() 
        if day == "All" or day in DAYS:
            print("Thank you, checking the day!")
            break
        else:
            print("Please choose a correct day")
    print("Checking day", day)

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
    
    #convert the start time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    
    # extract month and day of week from Start time to create new columns
    df["Month"] = df["Start Time"].dt.month
    
    if month != "All":
        month_index = MONTHS.index(month)
        df = df[df["Month"] == month_index + 1]
    
    df["Day"] = df["Start Time"].dt.day_name()
    
    if day != "All":  
        df = df[df["Day"] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    print(df['Month'].mode().size)
    if df['Month'].mode().size > 0:
        
        popular_month = df['Month'].mode()[0]
        
        print("Most popular month is: ", MONTHS[popular_month-1])

    # display the most common day of week
    
    popular_day = df['Day'].mode()[0]
    print("Most popular day is: ", popular_day)
    
    # display the most common start hour
    
    df["Hour"] = df["Start Time"].dt.hour
    popular_start_hour = df['Hour'].mode()[0]
    
    print("Most popular start hour is: ", popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def getstation(df, station):
    return df[station].mode()[0]

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print("Most popular start station is:", getstation(df, "Start Station"))
    
    # display most commonly used end station
    
    print("Most popular end station is:", getstation(df, "End Station"))

    # display most frequent combination of start station and end station trip

    both_stations = df["Start Station"] + " and " + df["End Station"]
    combination = both_stations.mode()[0]
    
    print("Most frequent combination of start and end station is:", combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    total_travel_time = df["Trip Duration"].sum()
    print(f"Total Minutes: {total_travel_time}, Total Hours: {total_travel_time/60:.0f}")    
    # display mean travel time

    average_travel_time = df["Trip Duration"].mean()
    print(f'Average minutes: {average_travel_time:.0f}')
    print(f'Average hours: {average_travel_time/60:.0f}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    print('-'*40)
    print("Show data for users split: \n")
    
    # Display counts of user types
    user_types = df["User Type"].unique()
    
    # For each user type print the sum of user type
    for user_type in user_types:
        if user_type and type(user_type) == str:
            print(f'{user_type}: {df["User Type"].str.count(user_type).sum():.0f}')

    
    print('-'*40)
    print("Show data for gender split: \n")
   
    # If gender is part of the data set get the unique genders and print the sum
    if "Gender" in df.columns:
        gender_types = df["Gender"].unique()
        
        for gender_type in gender_types:
            if gender_type and type(gender_type) == str:
                print(f'{gender_type}: {df["Gender"].str.count(gender_type).sum():.0f}')
    else:
        print("No data for gender")
    
    # Display earliest, most recent, and most common year of birth

    print('-'*40)
    print("Show data for age split: \n")
    
    if "Birth Year" in df.columns:
        oldest = df["Birth Year"].min()
        print(f"The oldest user age: {datetime.now().year-oldest:.0f}")
            
        youngest = df["Birth Year"].max()
        print(f"The youngest user age: {datetime.now().year-youngest:.0f}")

        popular_year = df["Birth Year"].mode()[0]
        print(f"The most common user age: {datetime.now().year-popular_year:.0f}")
        
    else:
        print("No data for birth year")

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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

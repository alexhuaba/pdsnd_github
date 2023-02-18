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
    
    #  get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Let´s choose a city. You can choose between chicago, new york city or washington. Where are you interested in?').lower()  
    while city != 'chicago' and city != 'washington' and city != 'new york city':
        print(city + " " + 'is not available!')
        city = input('Please select another city. You only can choose between chicago, new york city and washington.').lower()
    
    print(city)
    
    # get user input for month (all, january, february, ... , june)
    month = input('Now you have the chance to filter the data. Do you want to see data from a specific month, than please enter a month from january till june. If you want to see all datas, please enter "all"!').lower()
    while month != 'all' and month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june':
            print('This seems not possbile. Too see all data please enter "all". Or if you want to see data from specific months, please enter january till june!')
            month = input('please set another month!').lower()
    print(month)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Now please type in a day (eg. monday ... sunday), or if you wish to get information of every day type in "all"').lower()
    while day != 'all' and day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday':
            print('You can only choose between "all" or single days like "monday"')
            day = input('please check and type in "all" or a specific day!').lower()
    print(day)
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
   # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #generate a new hour collumn out of Start time
    df['hour'] = df['Start Time'].dt.hour
    #generate a new combined collumn out of Start and End Station
    df['combined'] = df['Start Station'] + " " + df['End Station'] 
   

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # add new collumns if city is washington
    print(city)
    if city == 'washington':
        df.insert(loc=2, column='Gender', value='no information')
        df.insert(loc=3, column='Birth Year', value='no information')
        
    return df

def view_raw_data(df):
    """ Asks the user if he wants to see some raw datas."""
    
    print('\nCalculating The Time for 5 rows of raw data...\n')
    start_time = time.time()
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:(start_loc + 5)])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # print(df)
    mostmonth = (df['month'].value_counts().idxmax())
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    mostmonth = months[mostmonth - 1]
    print('The most common month was' + " " + mostmonth)
      
    # display the most common day of week
    mostday = (df['day_of_week'].value_counts().idxmax())
    print('The most common day was' + " " + mostday)

    # display the most common start hour
      
    mosthour = df['hour'].mode()[0]
    print('The most common start hour was:',  mosthour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    #print(df)
    moststartstation = df['Start Station'].mode()[0]
    print('the most popular Start Station is:', moststartstation)
    
    # display most commonly used end station
    mostendstation = df['End Station'].mode()[0]
    print('the most popular End Station is:', mostendstation)

    # display most frequent combination of start station and end station trip
    combitrip = df['combined'].mode()[0]
    print('The most frequent combination of Start and End Station is:', combitrip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    totaltrip = df['Trip Duration'].sum()
    print('The total travel time is:')
    print(totaltrip)

    # display mean travel time
    meantrip = df['Trip Duration'].mean()
    print('The mean travel time is:')
    print(meantrip)
    
   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    
    gender = df['Gender'].mode()[0]  
    if gender == 'no information':
        print("Unfortunately we don´t have informations about gender count to this city.")
    else:
        print(df.groupby(['Gender'])['Gender'].count(), '\n')

    # Display earliest and most common year of birth
    mostcommonyear = df['Birth Year'].mode()[0]
    if mostcommonyear == 'no information':
        print("Unfortunately we don´t have statistics about birth years to this city.")
    else:
        mostcommonyear = df['Birth Year'].mode()[0]
        print('The most common year of birth is:', mostcommonyear)
        earliest = df['Birth Year'].min()
        print('The youngest persons are born in the year:', earliest)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

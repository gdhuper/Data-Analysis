import pandas as pd
import numpy as np


nyc_subway_weather = pd.read_csv("nyc_subway_weather.csv")

#nyc_subway_data = np.array(nyc_subway_weather)
print(nyc_subway_weather.head())
print(nyc_subway_weather.describe())

# Subway ridership for 5 stations on 10 different days
ridership = np.array([
    [0, 0, 2, 5, 0],
    [1478, 3877, 3674, 2328, 2539],
    [1613, 4088, 3991, 6461, 2691],
    [1560, 3392, 3826, 4787, 2613],
    [1608, 4802, 3932, 4477, 2705],
    [1576, 3933, 3909, 4979, 2685],
    [95, 229, 255, 496, 201],
    [2, 0, 1, 27, 0],
    [1438, 3785, 3589, 4174, 2215],
    [1342, 4043, 4009, 4665, 3033]
])

# Change False to True for each block of code to see what it does

# Accessing elements
if False:
    print
    ridership[1, 3]
    print
    ridership[1:3, 3:5]
    print
    ridership[1, :]

# Vectorized operations on rows or columns
if False:
    print
    ridership[0, :] + ridership[1, :]
    print
    ridership[:, 0] + ridership[:, 1]

# Vectorized operations on entire arrays
if False:
    a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    b = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    print
    a + b


'''def mean_riders_for_max_station(ridership):
    ''
    Fill in this function to find the station with the maximum riders on the
    first day, then return the mean riders per day for that station. Also
    return the mean ridership overall for comparsion.

    Hint: NumPy's argmax() function might be useful:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.argmax.html
    ''
    max_station = ridership[0, :].argmax()
    overall_mean = ridership.mean()
    mean_for_max = ridership[:, max_station].mean()

    return (overall_mean, mean_for_max)
'''

def min_and_max_riders_per_day(ridership):
    '''
    Fill in this function. First, for each subway station, calculate the
    mean ridership per day. Then, out of all the subway stations, return the
    maximum and minimum of these values. That is, find the maximum
    mean-ridership-per-day and the minimum mean-ridership-per-day for any
    subway station.
    '''
    station_riders = ridership.mean(axis=0)

    max_daily_ridership = station_riders.max()  # Replace this with your code
    min_daily_ridership = station_riders.min()  # Replace this with your code

    return (max_daily_ridership, min_daily_ridership)


#print(mean_riders_for_max_station(ridership))
print(min_and_max_riders_per_day(ridership))

#creating data frame in pandas
enrollment = pd.DataFrame({
    'account_key': [448, 44,334 ,34 ,434],
    'status' :['cancelled', 'cancelled', 'cancelled', 'cancelled', 'cancelled'],
    'days_to_cancel' : [4, 5, 6, 6, 6],
    'is_udacity': [True, True, True, True, False]
})



print(enrollment)
print(enrollment.values)

# Subway ridership for 5 stations on 10 different days
ridership_df = pd.DataFrame(
    data=[[0, 0, 2, 5, 0],
          [1478, 3877, 3674, 2328, 2539],
          [1613, 4088, 3991, 6461, 2691],
          [1560, 3392, 3826, 4787, 2613],
          [1608, 4802, 3932, 4477, 2705],
          [1576, 3933, 3909, 4979, 2685],
          [95, 229, 255, 496, 201],
          [2, 0, 1, 27, 0],
          [1438, 3785, 3589, 4174, 2215],
          [1342, 4043, 4009, 4665, 3033]],
    index=['05-01-11', '05-02-11', '05-03-11', '05-04-11', '05-05-11',
           '05-06-11', '05-07-11', '05-08-11', '05-09-11', '05-10-11'],
    columns=['R003', 'R004', 'R005', 'R006', 'R007']
)

# Change False to True for each block of code to see what it does

# DataFrame creation
if False:
    # You can create a DataFrame out of a dictionary mapping column names to values
    df_1 = pd.DataFrame({'A': [0, 1, 2], 'B': [3, 4, 5]})
    print
    df_1

    # You can also use a list of lists or a 2D NumPy array
    df_2 = pd.DataFrame([[0, 1, 2], [3, 4, 5]], columns=['A', 'B', 'C'])
    print
    df_2

# Accessing elements
if False:
    print
    ridership_df.iloc[0]
    print
    ridership_df.loc['05-05-11']
    print
    ridership_df['R003']
    print
    ridership_df.iloc[1, 3]

# Accessing multiple rows
if False:
    print
    ridership_df.iloc[1:4]

# Accessing multiple columns
if False:
    print
    ridership_df[['R003', 'R005']]

# Pandas axis
if False:
    df = pd.DataFrame({'A': [0, 1, 2], 'B': [3, 4, 5]})
    print
    df.sum()
    print
    df.sum(axis=1)
    print
    df.values.sum()


def mean_riders_for_max_station(ridership):
    '''
    Fill in this function to find the station with the maximum riders on the
    first day, then return the mean riders per day for that station. Also
    return the mean ridership overall for comparsion.

    This is the same as a previous exercise, but this time the
    input is a Pandas DataFrame rather than a 2D NumPy array.
    '''
    max_rider = ridership['R006'].mean()

    print(max_rider)
    overall_mean = ridership.values.mean()
    mean_for_max = ridership['R006'].mean()

    return (overall_mean, mean_for_max)

print(mean_riders_for_max_station(ridership_df))

grades_df = pd.DataFrame(
    data={'exam1': [43, 81, 78, 75, 89, 70, 91, 65, 98, 87],
          'exam2': [24, 63, 56, 56, 67, 51, 79, 46, 72, 60]},
    index=['Andre', 'Barry', 'Chris', 'Dan', 'Emilio',
           'Fred', 'Greta', 'Humbert', 'Ivan', 'James']
)

# Change False to True for this block of code to see what it does

# DataFrame apply()
if False:
    def convert_grades_curve(exam_grades):
        # Pandas has a bult-in function that will perform this calculation
        # This will give the bottom 0% to 10% of students the grade 'F',
        # 10% to 20% the grade 'D', and so on. You can read more about
        # the qcut() function here:
        # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.qcut.html
        return pd.qcut(exam_grades,
                       [0, 0.1, 0.2, 0.5, 0.8, 1],
                       labels=['F', 'D', 'C', 'B', 'A'])


    # qcut() operates on a list, array, or Series. This is the
    # result of running the function on a single column of the
    # DataFrame.
    print
    convert_grades_curve(grades_df['exam1'])

    # qcut() does not work on DataFrames, but we can use apply()
    # to call the function on each column separately
    print
    grades_df.apply(convert_grades_curve)


def standardize_column(column):
    return (column - column.mean()) / column.std(ddof=0)


def standardize(df):
    '''
    Fill in this function to standardize each column of the given
    DataFrame. To standardize a variable, convert each value to the
    number of standard deviations it is above or below the mean.
    '''
    return df.apply(standardize_column)
print(standardize(grades_df))
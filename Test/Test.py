import unicodecsv
from datetime import datetime as dt
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

## Longer version of code (replaced with shorter, equivalent version below)
# enrollments = []
# f = open('enrollments.csv', 'rb')
# reader = unicodecsv.DictReader(f)
# for row in reader:
#     enrollments.append(row)
# f.close()
def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

enrollments = read_csv("enrollments.csv")
daily_engagement = read_csv("daily_engagement.csv")
project_submissions = read_csv("project_submissions.csv")


### For each of these three tables, find the number of rows in the table and
### the number of unique students in the table. To find the number of unique
### students, you might want to create a set of the account keys in each table.



# Takes a date as a string, and returns a Python datetime object.
# If there is no date given, returns None
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%Y-%m-%d')


# Takes a string which is either an empty string or represents an integer,
# and returns an int or None.
def parse_maybe_int(i):
    if i == '':
        return None
    else:
        return int(i)

for engagement_record in daily_engagement:
    engagement_record['account_key'] = engagement_record['acct']
    del [engagement_record['acct']]

# Clean up the data types in the enrollments table
for enrollment in enrollments:
    enrollment['cancel_date'] = parse_date(enrollment['cancel_date'])
    enrollment['days_to_cancel'] = parse_maybe_int(enrollment['days_to_cancel'])
    enrollment['is_canceled'] = enrollment['is_canceled'] == 'True'
    enrollment['is_udacity'] = enrollment['is_udacity'] == 'True'
    enrollment['join_date'] = parse_date(enrollment['join_date'])

for engagement_record in daily_engagement:
    engagement_record['lessons_completed'] = int(float(engagement_record['lessons_completed']))
    engagement_record['num_courses_visited'] = int(float(engagement_record['num_courses_visited']))
    engagement_record['projects_completed'] = int(float(engagement_record['projects_completed']))
    engagement_record['total_minutes_visited'] = float(engagement_record['total_minutes_visited'])
    engagement_record['utc_date'] = parse_date(engagement_record['utc_date'])

for submission in project_submissions:
    submission['completion_date'] = parse_date(submission['completion_date'])
    submission['creation_date'] = parse_date(submission['creation_date'])




def get_unique_students(data):
    unique_students = set()
    for data_point in data:
        unique_students.add(data_point['account_key'])
    return unique_students

enrollment_num_rows = len(enrollments)
enrollment_num_unique_students = get_unique_students(enrollments)  # Replace this with your code


engagement_num_rows = len(daily_engagement)
engagement_num_unique_students = get_unique_students(daily_engagement) # Replace this with your code

submission_num_rows = len(project_submissions)
submission_num_unique_students = get_unique_students(project_submissions)  # Replace this with your code


# unique students
num_problem_students = 0
num_pro_students = set()
for i in enrollments:
    student = i['account_key']
    if student not in engagement_num_unique_students and i['join_date'] != i['cancel_date']:
        num_problem_students += 1
        num_pro_students.add(student)


#weeding out udacity test accounts
udacity_test_accounts = set()
for enrollment in enrollments:
    if enrollment['is_udacity']:
        udacity_test_accounts.add(enrollment['account_key'])


def remove_udacity_accounts(data):
    non_udacity_data = []
    for data_point in data:
        if data_point['account_key'] not in udacity_test_accounts:
            non_udacity_data.append(data_point)
    return non_udacity_data



non_udacity_enrollments = remove_udacity_accounts(enrollments)
non_udacity_engagement = remove_udacity_accounts(daily_engagement)
non_udacity_submissions = remove_udacity_accounts(project_submissions)


# calculating paid students
paid_students = {}
for enrollment in non_udacity_enrollments:
    if not enrollment['is_canceled'] or enrollment['days_to_cancel'] > 7:
        account_key = enrollment['account_key']
        enrollment_date = enrollment['join_date']
        if account_key not in paid_students or enrollment_date > paid_students[account_key]:
            paid_students[account_key] = enrollment_date

print("paid students: " + str(len(paid_students)))

# Takes a student's join date and the date of a specific engagement record,
# and returns True if that engagement record happened within one week
# of the student joining.
def within_one_week(join_date, engagement_date):
    time_delta = engagement_date - join_date
    return time_delta.days < 7 and time_delta.days >= 0

def remove_free_trial_cancels(data):
    new_data = []
    for data_point in data:
        if data_point['account_key'] in paid_students:
            new_data.append(data_point)

    return new_data

paid_enrollments = remove_free_trial_cancels(non_udacity_enrollments)
paid_engagement = remove_free_trial_cancels(non_udacity_engagement)
paid_submissions = remove_free_trial_cancels(non_udacity_submissions)

print(len(paid_enrollments))
print(len(paid_engagement))
print(len(paid_submissions))


for engagement_record in paid_engagement:
    if engagement_record['num_courses_visited'] > 0:
        engagement_record['has_visited'] = 1
    else:
        engagement_record['has_visited'] = 0


# calculating paid students for engagement
paid_engagement_in_first_week = []

for engagement_record in paid_engagement:
    account_key = engagement_record['account_key']
    join_date = paid_students[account_key]
    engagement_record_date = engagement_record['utc_date']

    if within_one_week(join_date, engagement_record_date):
        paid_engagement_in_first_week.append(engagement_record)


print("paid engagement in first week :" + str(len(paid_engagement_in_first_week)))

# Create a dictionary of engagement grouped by student.
# The keys are account keys, and the values are lists of engagement records.
def group_data(data, key_name):
    grouped_data = defaultdict(list)
    for data_point in data:
        key = data_point[key_name]
        grouped_data[key].append(data_point)
    return grouped_data

engagement_by_account = group_data(paid_engagement_in_first_week, 'account_key')





# Create a dictionary with the total minutes each student spent in the classroom during the first week.
# The keys are account keys, and the values are numbers (total minutes)
def sum_grouped_items(grouped_data, field_name):
    summed_data = {}
    for key, data_points in grouped_data.items():
        total = 0
        for data_point in data_points:
            total += data_point[field_name]
        summed_data[key] = total

    return summed_data



total_minutes_by_account = sum_grouped_items(engagement_by_account, 'total_minutes_visited')
total_lessons_by_account = sum_grouped_items(engagement_by_account, 'lessons_completed')
days_visited_by_account = sum_grouped_items(engagement_by_account, 'has_visited')

total_lessons = list(total_lessons_by_account.values())
total_minutes = list(total_minutes_by_account.values())
total_days_visited = list(days_visited_by_account.values())

def describe_data(data, title):
    print('Mean :', np.mean(data))
    print('Standard deviation :', np.std(data))
    print('Minimum: ', np.min(data))
    print('Maximum: ', np.max(data))
    plt.hist(data, bins=8)
    plt.title(title)
    plt.show()



subway_project_lesson_keys = ['746169184', '3176718735']

pass_subway_project = set()


for student in paid_submissions:
    if student['lesson_key'] in subway_project_lesson_keys and (student['assigned_rating'] == 'PASSED' or student['assigned_rating'] == 'DISTINCTION'):
        pass_subway_project.add(student['account_key'])


passing_engagement = []
non_passing_engagement = []

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] in pass_subway_project:
        passing_engagement.append(engagement_record)
    else:
        non_passing_engagement.append(engagement_record)

print(len(pass_subway_project))

print(len(passing_engagement))
print(len(non_passing_engagement))


passing_engagement_by_account = group_data(passing_engagement, 'account_key')
non_passing_engagement_by_account = group_data(non_passing_engagement, 'account_key')

passing_minutes = sum_grouped_items(passing_engagement_by_account, 'total_minutes_visited')
non_passing_minutes = sum_grouped_items(non_passing_engagement_by_account, 'total_minutes_visited')

describe_data(list(non_passing_minutes.values()), 'Non-Passing Minutes')
describe_data(list(passing_minutes.values()), 'Passing Minutes')


#priting stats
describe_data(total_minutes, 'Total Minutes')
print("printing stats for lessons completed")
describe_data(total_lessons, 'Total Lessons')
print("printing stats for days visited \n")
describe_data(total_days_visited, 'Total days visited')
# debugging find student with max minutes
'''student_with_max_minutes = None
max_minutes = 0
for student, total_minutes in total_minutes_by_account.items():
    if total_minutes > max_minutes:
        max_minutes = total_minutes
        student_with_max_minutes = student

for engagement_record in paid_engagement_in_first_week:
    if engagement_record['account_key'] == student_with_max_minutes:
        print(engagement_record)
'''



#printing stats
print("total enrolled: " + str(enrollment_num_rows))
print("total engaged: " + str(engagement_num_rows))
print("total submissions: " + str(submission_num_rows))
print("enrollment_unique: " + str(len(enrollment_num_unique_students)))
print("submission_unique: " + str(len(submission_num_unique_students)))
print("engagement_unique: " + str(len(engagement_num_unique_students)))
print("num_prob_students: " + str(num_problem_students))

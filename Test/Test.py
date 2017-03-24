import unicodecsv
from datetime import datetime as dt

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

enrollment_num_rows = 0  # Replace this with your code
for i in enrollments:
    enrollment_num_rows += 1

print (enrollment_num_rows)
enrollment_num_unique_students = 0  # Replace this with your code
templist = []
for i in enrollments:
    if i['account_key'] not in templist:
        templist.append(i['account_key'])
        enrollment_num_unique_students += 1
    else:
        continue

print (enrollment_num_unique_students)

engagement_num_rows = 0  # Replace this with your code

for i in daily_engagement:
    engagement_num_rows += 1
print (engagement_num_rows)

templist2 = []
engagement_num_unique_students = 0  # Replace this with your code
for i in daily_engagement:
    if i['acct'] not in templist2:
        templist2.append(i['acct'])
        engagement_num_unique_students += 1
    else:
        continue

print (engagement_num_unique_students)

submission_num_rows = 0  # Replace this with your code
templist3 = []
for i in project_submissions:
    submission_num_rows += 1
print (submission_num_rows)

submission_num_unique_students = 0  # Replace this with your code
for i in project_submissions:
    if i['account_key'] not in templist3:
        templist3.append(i['account_key'])
        submission_num_unique_students += 1
    else:
        continue

print (submission_num_unique_students)
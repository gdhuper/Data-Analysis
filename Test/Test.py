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

enrollment_num_rows = 0  # Replace this with your code
for i in enrollments:
    enrollment_num_rows += 1

print (enrollment_num_rows)
enrollment_num_unique_students = len(get_unique_students(enrollments))  # Replace this with your code

print ("enrollment_unique " + str(enrollment_num_unique_students))

engagement_num_rows = 0  # Replace this with your code

for i in daily_engagement:
    engagement_num_rows += 1
print (engagement_num_rows)


engagement_num_unique_students = get_unique_students(daily_engagement) # Replace this with your code

print ("engagement_unique " + str(len(engagement_num_unique_students)))

submission_num_rows = 0  # Replace this with your code
for i in project_submissions:
    submission_num_rows += 1
print (submission_num_rows)

submission_num_unique_students = len(get_unique_students(project_submissions))  # Replace this with your code

print ("submission_unique " + str(submission_num_unique_students))

num_problem_students = 0

for i in enrollments:
    student = i['account_key']
    if student not in engagement_num_unique_students and i['join_date'] != i['cancel_date']:
        num_problem_students += 1


print("num_prob_students: " + str(num_problem_students))
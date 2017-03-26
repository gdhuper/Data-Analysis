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
        paid_students[account_key] = enrollment_date
        
print("paid students: " + str(len(paid_students)))




#printing stats
print("total enrolled: " + str(enrollment_num_rows))
print("total engaged: " + str(engagement_num_rows))
print("total submissions: " + str(submission_num_rows))
print("enrollment_unique: " + str(len(enrollment_num_unique_students)))
print("submission_unique: " + str(len(submission_num_unique_students)))
print("engagement_unique: " + str(len(engagement_num_unique_students)))
print("num_prob_students: " + str(num_problem_students))

import subprocess

input_text = """admin
password
1
1
student
SR123454
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact
1
student
SR123456
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact
1
student
SR123457
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact
1
student
SR123458
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact
1
student
SR123459
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact
1
student
SR123451
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact
1
student
SR123452
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact
1
student
SR12343
Computer Science
Block A
John
Doe
M
1990-01-01
john.doe@email.com
123 Main St.
555-1234
555-5678
Emergency Contact"""

with open('input.txt', 'w') as f:
    f.write(input_text)

subprocess.run(["python", "src\EduTrack.py"], text=True, input=input_text)

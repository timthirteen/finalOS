Students Database API
This is a simple Flask API that allows you to interact with a PostgreSQL database containing information about students. You can perform basic CRUD (Create, Read, Update, Delete) operations on the students' data.

final_project/ backend -> app.py frontend -> Static frontend files (hosted in S3)

1. Set up EC2 Instance:
``Configure the security group to allow traffic on ports: 80, 22, 443, 5432, 8000, and all traffic. Set up RDS PostgreSQL:``

Make sure the RDS instance allows all traffic from the EC2 instance (public access). SSH into EC2:

2.Run:``` ssh -i "C:\your_key_2_ec2.pem" ubuntu@<EC2_Public_IP>```

3. Install dependencies:

```sudo apt update
sudo apt install python3 python3-pip postgresql-client -y
Connect to the RDS instance using psql: psql -h <RDS_End_Point> -U <RDS_User> -d <RDS_Database_Name>
```

4.Your PostgreSQL table tbl_mahmud_data should look like this:
```CREATE TABLE table_timur (
    student_id SERIAL PRIMARY KEY,  -- Auto-incrementing ID for each student
    full_name VARCHAR(255) NOT NULL, -- Student's full name
    gender VARCHAR(50),             -- Student's gender
    age INT,                        -- Student's age
    department VARCHAR(100),        -- Department the student belongs to
    gpa DECIMAL(3, 2),              -- GPA with two decimal places
    enrollment_year INT             -- The year the student enrolled
);
```
5.
```
mkdir project
cd project
touch app.py

```

6.use python file 
7.Edit app.py and implement the Flask application with PostgreSQL connection.
Create index.html Template: Create and populate index.html to display the tbl_mahmud_data.

8.Install Python Dependencies: Install python3-venv (if not already installed)

cd final_project
sudo apt update
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate

9.Run pthon 
``` python app.py```





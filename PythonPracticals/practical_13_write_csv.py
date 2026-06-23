import csv

data = [
    ["Name", "Department", "Salary", "City"],
    ["Aishwarya Desai", "IT", 45000, "Pune"],
    ["Rohit Mane", "HR", 38000, "Mumbai"],
    ["Meghna Patil", "Finance", 52000, "Aurangabad"],
    ["Nilima Jadhav", "IT", 47000, "Nashik"],
    ["Pravin Shinde", "Admin", 35000, "Nagpur"],
    ["Shital More", "Finance", 55000, "Pune"]
]

try:
    with open("employees.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print("Student: Aishwarya | CSV file written successfully.")
except IOError as e:
    print(f"Student: Aishwarya | Error writing CSV: {e}")

new_employee = ["Rahul Kulkarni", "IT", 49000, "Mumbai"]
try:
    with open("employees.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_employee)
    print("Student: Rohit | New record appended.")
except IOError as e:
    print(f"Student: Rohit | Error appending to CSV: {e}")

try:
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        print("Student: Meghna | Employee Records:")
        for row in reader:
            print(row)
except FileNotFoundError:
    print("Student: Meghna | Error: employees.csv not found.")
except csv.Error as e:
    print(f"Student: Meghna | Error reading CSV: {e}")

try:
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        it_employees = [row for row in reader if row["Department"] == "IT"]
    print("Student: Nilima | IT Department Employees:")
    for emp in it_employees:
        print(emp["Name"], "-", emp["Salary"])
except FileNotFoundError:
    print("Student: Nilima | Error: employees.csv not found.")
except KeyError as e:
    print(f"Student: Nilima | Error: Missing column {e} in CSV.")
except csv.Error as e:
    print(f"Student: Nilima | Error reading CSV: {e}")

try:
    with open("employees.csv", "r") as file:
        reader = csv.DictReader(file)
        salaries = [int(row["Salary"]) for row in reader]
    print("Student: Pravin | Total Salary:", sum(salaries))
    print("Student: Shital | Average Salary:", sum(salaries)/len(salaries))
except FileNotFoundError:
    print("Error: employees.csv not found.")
except (KeyError, ValueError) as e:
    print(f"Error processing salary data: {e}")
except csv.Error as e:
    print(f"Error reading CSV: {e}")

import csv

students = [
    ["Name", "Age", "City", "Marks"],
    ["Amruta Jadhav", 21, "Aurangabad", 88],
    ["Rajesh Kulkarni", 22, "Pune", 76],
    ["Sunanda More", 20, "Nashik", 91],
    ["Ketan Pawar", 23, "Mumbai", 83],
    ["Varsha Shinde", 21, "Nagpur", 79]
]

try:
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(students)
    print("CSV file created.")
except IOError as e:
    print(f"Error creating CSV file: {e}")

try:
    with open("students.csv", "r") as file:
        reader = csv.reader(file)
        print("Student: Amruta | All Records:")
        for row in reader:
            print(row)
except FileNotFoundError:
    print("Error: students.csv not found.")
except csv.Error as e:
    print(f"Error reading CSV: {e}")

try:
    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)
        print("Student: Rajesh | Name and Marks:")
        for row in reader:
            print(row["Name"], "->", row["Marks"])
except FileNotFoundError:
    print("Error: students.csv not found.")
except KeyError as e:
    print(f"Error: Missing column {e} in CSV.")
except csv.Error as e:
    print(f"Error reading CSV: {e}")

try:
    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)
        marks = [int(row["Marks"]) for row in reader]
    print("Student: Sunanda | Max Marks:", max(marks))
    print("Student: Ketan | Min Marks:", min(marks))
    print("Student: Varsha | Average Marks:", sum(marks)/len(marks))
except FileNotFoundError:
    print("Error: students.csv not found.")
except (KeyError, ValueError) as e:
    print(f"Error processing marks data: {e}")
except csv.Error as e:
    print(f"Error reading CSV: {e}")

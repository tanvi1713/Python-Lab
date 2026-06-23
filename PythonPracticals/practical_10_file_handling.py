import os

try:
    file = open("vijay_data.txt", "w")
    file.write("Name: Vijay Shinde\n")
    file.write("City: Aurangabad\n")
    file.write("Course: BCA\n")
    file.close()
    print("Student: Vijay | File written successfully.")
except IOError as e:
    print(f"Student: Vijay | Error writing file: {e}")

try:
    file = open("vijay_data.txt", "r")
    content = file.read()
    file.close()
    print("Student: Sarika | File Content:\n", content)
except FileNotFoundError:
    print("Student: Sarika | Error: File not found.")
except IOError as e:
    print(f"Student: Sarika | Error reading file: {e}")

try:
    file = open("vijay_data.txt", "a")
    file.write("Marks: 88\n")
    file.close()
    print("Student: Omkar | Data appended.")
except IOError as e:
    print(f"Student: Omkar | Error appending to file: {e}")

try:
    with open("vijay_data.txt", "r") as file:
        lines = file.readlines()
    print("Student: Omkar | Lines in file:")
    for line in lines:
        print(line.strip())
except FileNotFoundError:
    print("Student: Omkar | Error: File not found.")
except IOError as e:
    print(f"Student: Omkar | Error reading file: {e}")

if os.path.exists("vijay_data.txt"):
    print("File exists.")
else:
    print("File not found.")

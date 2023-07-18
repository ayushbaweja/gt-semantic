import json

# Load the JSON data
with open('202302.json') as file:
    data = json.load(file)

# Filter and extract required information
filtered_data = {}
for course_code, course_info in data['courses'].items():
    course_name = course_info[0]
    course_desc = course_info[-1]
    filtered_data[course_code] = {
        'course_name': course_name,
        'course_desc': course_desc
    }

# Save the filtered data to a new JSON file
with open('output.json', 'w') as file:
    json.dump(filtered_data, file, indent=2)
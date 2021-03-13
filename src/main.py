import json

separator = "="
project_properties = {}

with open('../project.properties') as f:

    for line in f:
        if separator in line:

            name, value = line.split(separator, 1)

            project_properties[name.strip()] = value.strip()

code_results = []
blank_results = []
comment_results = []

project_name = project_properties.get('project.name')

input_json_file = '../tmp/' + project_name + '-raw.json'

with open(input_json_file) as json_file:
    rawResults = json.load(json_file)

for i in range(0, len(rawResults)):
    for j in range(0, len(rawResults[i].get('Files'))):
        code_results.append({
            'name': rawResults[0].get('Files')[0].get('Name'),
            'category': 'Code',
            'file': rawResults[0].get('Files')[0].get('Location'),
            'value': rawResults[0].get('Files')[0].get('Code'),
        })

        blank_results.append({
            'name': rawResults[0].get('Files')[0].get('Name'),
            'category': 'Blank',
            'file': rawResults[0].get('Files')[0].get('Location'),
            'value': rawResults[0].get('Files')[0].get('Blank'),
        })

        comment_results.append({
            'name': rawResults[0].get('Files')[0].get('Name'),
            'category': 'Comment',
            'file': rawResults[0].get('Files')[0].get('Location'),
            'value': rawResults[0].get('Files')[0].get('Comment'),
        })

dx_results = code_results + blank_results + comment_results

output_json_file = '../out/' + project_name + '-results.json'

with open(output_json_file, 'w') as outfile:
    json.dump(dx_results, outfile)

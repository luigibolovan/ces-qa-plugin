import json

properties_separator = '='
lang_separator = ','
accepted_langs_separator = ' ('
project_properties = {}

with open('../project.properties') as f:
    for line in f:
        if properties_separator in line:
            name, value = line.split(properties_separator, 1)
            project_properties[name.strip()] = value.strip()

code_results = []
blank_results = []
comment_results = []

project_lang = project_properties.get('project.lang')
langs = project_lang.split(lang_separator)

lowercase_langs = []

for elem in langs:
    lowercase_langs.append(elem.lower())

raw_accepted_languages = []

with open('../cfg/languages.cfg') as f:
    for line in f:
        if accepted_langs_separator in line:
            lang, ext = line.split(accepted_langs_separator, 1)
            raw_accepted_languages.append(lang.lower())

project_name = project_properties.get('project.name')
project_path = project_properties.get('project.path')

input_json_file = '../tmp/' + project_name + '-raw.json'

with open(input_json_file) as json_file:
    raw_results = json.load(json_file)

unaccepted_langs = []

for elem in lowercase_langs:
    if elem not in raw_accepted_languages:
        unaccepted_langs.append(elem)

if len(unaccepted_langs) > 0:
    print('The following languages are not supported:', unaccepted_langs)

for i in range(0, len(raw_results)):
    for j in range(0, len(raw_results[i].get('Files'))):
        if raw_results[i].get('Files')[j].get('Language').lower() in lowercase_langs and raw_results[i].get('Files')[j].get('Language').lower() in raw_accepted_languages:
            file_path = raw_results[i].get('Files')[j].get('Location').replace(project_path + '/', '')
            code_results.append({
                'name': raw_results[i].get('Files')[j].get('Language'),
                'category': 'Code',
                'file': file_path,
                'value': raw_results[i].get('Files')[j].get('Code'),
            })

            blank_results.append({
                'name': raw_results[i].get('Files')[j].get('Language'),
                'category': 'Blank',
                'file': file_path,
                'value': raw_results[i].get('Files')[j].get('Blank'),
            })

            comment_results.append({
                'name': raw_results[i].get('Files')[j].get('Language'),
                'category': 'Comment',
                'file': file_path,
                'value': raw_results[i].get('Files')[j].get('Comment'),
            })

dx_results = code_results + blank_results + comment_results

output_json_file = '../out/' + project_name + '-results.json'

with open(output_json_file, 'w') as outfile:
    json.dump(dx_results, outfile, indent=4)



import json

properties_separator = '='
lang_separator = ','
accepted_langs_separator = ' ('
project_properties = {}
code_results = []
blank_results = []
comment_results = []
lowercase_langs = []
raw_accepted_languages = []
unaccepted_langs = []


def get_project_properties():
    with open('../cfg/project.properties') as f:
        for line in f:
            if properties_separator in line:
                name, value = line.split(properties_separator, 1)
                project_properties[name.strip()] = value.strip()


def lowercase_langs_letters(lang_list):
    for elem in lang_list:
        lowercase_langs.append(elem.lower())


def get_accepted_langs():
    with open('../data/languages.data') as f:
        for line in f:
            if accepted_langs_separator in line:
                lang, ext = line.split(accepted_langs_separator, 1)
                raw_accepted_languages.append(lang.lower())


def get_raw_json(input_file):
    with open(input_file) as json_file:
        results = json.load(json_file)
        return results


def verify_accepted_langs():
    for elem in lowercase_langs:
        if elem not in raw_accepted_languages:
            unaccepted_langs.append(elem)


def modify_json_format():
    for i in range(0, len(raw_results)):
        for j in range(0, len(raw_results[i].get('Files'))):
            if (raw_results[i].get('Files')[j].get('Language').lower() in lowercase_langs and
                    raw_results[i].get('Files')[j].get('Language').lower() in raw_accepted_languages) or \
                    (len(lowercase_langs) == 0):
                if '/' in raw_results[i].get('Files')[j].get('Location'):
                    file_path = raw_results[i].get('Files')[j].get('Location').replace(project_path + '/', '')
                elif '\\' in raw_results[i].get('Files')[j].get('Location'):
                    file_path_cut = raw_results[i].get('Files')[j].get('Location').replace(project_path + '\\', '')
                    file_path = file_path_cut.replace('\\', '/')
                else:
                    file_path = raw_results[i].get('Files')[j].get('Location')
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


def generate_new_json(output_file, results):
    with open(output_file, 'w') as outfile:
        json.dump(results, outfile, indent=4)


get_project_properties()

if 'project.name' in project_properties:
    if project_properties.get('project.name') != '':
        project_name = project_properties.get('project.name')
    else:
        project_name = 'unnamed'
else:
    project_name = 'unnamed'

project_path = project_properties.get('project.path')

if 'project.lang' in project_properties:
    if project_properties.get('project.lang') != '':
        project_lang = project_properties.get('project.lang')
        langs = project_lang.split(lang_separator)
    else:
        langs = ''
else:
    langs = ''

lowercase_langs_letters(langs)

get_accepted_langs()

input_json_file = '../tmp/' + project_name + '-raw.json'

raw_results = get_raw_json(input_json_file)

if not (len(langs) == 0):
    verify_accepted_langs()

if len(unaccepted_langs) > 0:
    print('The following languages are not supported:', unaccepted_langs)

modify_json_format()

dx_results = code_results + blank_results + comment_results

output_json_file = '../out/' + project_name + '-results.json'

generate_new_json(output_json_file, dx_results)

import re

from requests import request

def translate_google_operator(google_operator):
    if not google_operator:
        return None
    if ':' not in google_operator:
        return google_operator
    
    operator, search_string = google_operator.split(':', 1)
    if operator == 'inurl':
        return f'{search_string}.*'
    elif operator == 'intitle':
        return f'.*{search_string}.*'
    elif operator == 'site':
        return f'^{search_string}$'
    elif operator == 'intext':
        return f'.*{search_string}.*'
    elif operator == 'allintitle':
        return f'^{search_string}.*'
    return None    


def translate_search_expression(search_expression):
    search_expressions = search_expression.strip().split('\n')
    def translate_google_operator(google_operator):
        operator, search_string = google_operator.split(':', 1)
        operator = operator.strip().lower()
        search_string = search_string.strip()
        if operator == 'inurl':
            return re.compile(f'.*{search_string}.*', re.IGNORECASE)
        elif operator == 'intitle':
            return re.compile(f'^{search_string}$', re.IGNORECASE)
        elif operator == 'site':
            return re.compile(f'^{search_string}$', re.IGNORECASE)
        elif operator == 'intext':
            return re.compile(f'.*{search_string}.*', re.IGNORECASE)
        elif operator == 'allintitle':
            return re.compile(f'^{search_string}$', re.IGNORECASE)
        else:
            return None
    
    regexes = {}
    for se in search_expressions:
        if '|' in se:
            se = se.split('|')
            operator, search_string = se[0].strip().split(':', 1)
            operator = operator.strip().lower()
            search_string = search_string.strip()
            if operator not in regexes:
                regexes[operator] = []
            regexes[operator].append(re.compile(f'^{search_string}$', re.IGNORECASE))
        else:
            regex = translate_google_operator(se)
            if regex:
                operator, _ = se.split(':', 1)
                operator = operator.strip().lower()
                if operator not in regexes:
                    regexes[operator] = []
                regexes[operator].append(regex)
    return regexes

def merge_dicts(dict1, dict2):
    result = {}
    for key in set(dict1.keys()).union(dict2.keys()):
        if key in dict1 and key in dict2:
            result[key] = dict1[key] + dict2[key]
        elif key in dict1:
            result[key] = dict1[key]
        else:
            result[key] = dict2[key]
    return result


def accumulate_regexes():
    regexes = {}
    with open('google_search_operators', 'r',  encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '': continue 
            if(line.startswith('==') ): continue 
            search_expression = line.strip()
            line.replace("|"," ")
            regex = translate_search_expression(search_expression)
            if regex is None:
                print(f'Failed to translate Google search expression: {search_expression}')
            else:
                for key, value in regex.items():
                    if key in regexes:
                        regexes[key] += value
                    else:
                        regexes[key] = value
            merge_dicts(regexes, regex)
               
    return regexes

def test_translate_search_expression():
    with open('google_search_operators', 'r',  encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '': continue 
            if(line.startswith('==') ): continue 
            search_expression = line.strip()
            line.replace("|"," ")
            regex = translate_search_expression(search_expression)
            if regex is None:
                print(f'Failed to translate Google search expression: {search_expression}')
            else:
                print(f'Google search expression: {search_expression} -> Regular expression: {regex}')
               
    return regex



if __name__ == '__main__':
    
    
    dict = accumulate_regexes()
    if dict:
        print("Only urls:{}".format(dict))
    else:
        print("No dictionary returned.")

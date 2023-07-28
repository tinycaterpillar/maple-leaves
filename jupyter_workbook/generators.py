import os
import nbformat as nbf

def ktx_to_dict(input_file, keystarter='<'):
    """ parsing keyed text to a python dictionary. """
    answer = dict()

    with open(input_file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()

    k, val = '', ''
    for line in lines:
        if line.startswith(keystarter):
            k = line.replace(keystarter, '').strip()
            val = ''
        else:
            val += line

        if k:
            answer.update({k: val.strip()})

    return answer

HEADERS = ktx_to_dict(os.path.join('source', 'headers.ktx'))
QHA = ktx_to_dict(os.path.join('source', 'exercises.ktx'))

def create_jupyter_notebook(destination_filename='Exercises.ipynb'):
    """ Programmatically create jupyter notebook with the questions (and hints and solutions if required)
    saved under source files """

    # Create cells sequence
    nb = nbf.v4.new_notebook()

    nb['cells'] = []

    # - Add header:
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["sub_header"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["jupyter_instruction"]))
    nb['cells'].append(nbf.v4.new_markdown_cell(HEADERS["jupyter_shotcuts"]))

    # - Add initialisation
    nb['cells'].append(nbf.v4.new_code_cell('%run initialise.py'))

    # - Add questions and empty spaces for answers
    for n in range(1, len(QHA)//3+1):
        nb['cells'].append(nbf.v4.new_markdown_cell(f'#### {n}. ' + QHA[f'q{n}']))
        nb['cells'].append(nbf.v4.new_code_cell(""))

    # Delete file if one with the same name is found
    if os.path.exists(destination_filename):
        os.remove(destination_filename)

    # Write sequence to file
    nbf.write(nb, destination_filename)

if __name__ == '__main__':
    create_jupyter_notebook()
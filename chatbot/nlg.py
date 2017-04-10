import json
from jinja2 import Template

__author__ = 'mukundmk'

templates = dict()
with open('templates.txt') as f:
    templates = json.load(f)

for key_ in templates:
    templates[key_] = Template(templates[key_])


def generate_sentence(key, data):
    """
    Input: the template key and the data to fill the template
    Output: hindi sentence
    """

    global templates

    return templates[key].render(data)

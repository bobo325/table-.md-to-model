# from .tools import tableparse
import re
import sublime
import sublime_plugin
from sublime import Region


def convert_type(column_type):
    pattern = re.compile(r'varchar\((\d+)\)', re.S)
    m = pattern.match(column_type)
    if m:
        length = m.groups()[0]
        db_type = 'String({})'.format(length)
        return db_type
    mapper = {
        'bigint': 'BigInteger',
        'text': 'Text',
        'int': 'Integer',
        'bool': 'Boolean',
        'float': 'Float',
        'date': 'Date',
        'datetime': 'DateTime'
    }
    db_type = mapper.get(column_type, None)
    return db_type


def generate_column(column):
    column_template = ''
    column_name = column['column_name']
    column_type = column['column_type']
    column_desc = column['column_desc']
    if column_name == 'id' and column_type == 'bigint':
        column_template = '    # {}\n' \
            '    id = db.Column(db.BigInteger, ' \
            'primary_key=True, autoincrement=True)\n'.format(column_desc)
    else:
        db_type = convert_type(column_type)
        if not db_type:
            column_template += '    # TODO!!!: type not matched!\n'

        column_template += '    # {}\n'.format(column_desc)
        column_template += '    {} = db.Column(db.{})\n'.format(
            column_name, db_type)
    return column_template


def parse(content):
    """parse content."""
    lines = content.split('\n')
    table_list = []
    pattern = re.compile(r'##(.+?)[（\(](.+?)[）\)]', re.S)
    index = -1
    for line in lines:

        if line.startswith('##'):
            # table name
            s = pattern.search(line)
            if s:
                table_desc = s.groups()[0].strip()
                table_name = s.groups()[1].strip()
                table_dict = {
                    'table_name': table_name,
                    'table_desc': table_desc,
                    'columns': []
                }
                table_list.append(table_dict)
                index += 1
        if line.startswith('|'):
            # column
            units = line.split('|')
            std_units = [unit.strip() for unit in units[1:]]
            if std_units[0] \
                    and '列' not in std_units[0] \
                    and not std_units[0].startswith('-'):
                column_info = {
                    'column_name': std_units[0],
                    'column_type': std_units[1],
                    'column_desc': std_units[2]
                }
                table_list[index]['columns'].append(column_info)
    return table_list


def generate_template(table_list):
    main_template = ''
    for table in table_list:
        table_name = table['table_name']
        table_desc = table['table_desc']
        table_class = ''.join(
            [sub.title() for sub in table_name.split('_')])

        model_template = 'class {}(db.Model):\n' \
            '    """{}."""\n' \
            '    __tablename__ = \'{}\'\n'.format(
                table_class, table_desc, table_name)

        for column in table['columns']:
            column_template = generate_column(column)
            model_template += column_template
        model_template += '\n\n'
        main_template += model_template
    return main_template


def convert(content):
    table_list = parse(content)
    template = generate_template(table_list)
    return template


class tabletomodelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        size = self.view.size()
        content = self.view.substr(Region(0, size))
        template = convert(content).strip('\n') + '\n'

        # insert into new file in cureent window
        window = sublime.active_window()
        new_view = window.new_file()

        new_view.insert(edit, 0, template)
        new_view.set_syntax_file('Packages/Python/Python.sublime-syntax')

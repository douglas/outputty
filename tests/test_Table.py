#!/usr/bin/env python
# coding: utf-8

# Copyright 2011 Álvaro Justen
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from textwrap import dedent

import unittest
import tempfile
import os
import sys

sys.path.insert(0, '..')
from outputty import Table


class TestTable(unittest.TestCase):
    def test_table_with_only_one_header_without_data(self):
        my_table = Table(headers=['test'])
        self.assertEqual(str(my_table), dedent('''
        +------+
        | test |
        +------+
        ''').strip())
        my_table = Table(headers=['blabla'])
        self.assertEqual(str(my_table), dedent('''
        +--------+
        | blabla |
        +--------+
        ''').strip())

    def test_table_with_many_headers_without_data(self):
        my_table = Table(headers=['spam', 'ham'])
        self.assertEqual(str(my_table), dedent('''
        +------+-----+
        | spam | ham |
        +------+-----+
        ''').strip())
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        ''').strip())

    def test_table_with_many_headers_and_one_row_same_size(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 123, 'spam': 4567, 'eggs': 8910})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        | 123 | 4567 | 8910 |
        +-----+------+------+
        ''').strip())

    def test_table_with_many_headers_and_rows_same_size(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 123, 'spam': 4567, 'eggs': 8910})
        my_table.rows.append({'ham': 321, 'spam': 7654, 'eggs': 1098})
        my_table.rows.append({'ham': 'abc', 'spam': 'defg', 'eggs': 'hijk'})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        | 123 | 4567 | 8910 |
        | 321 | 7654 | 1098 |
        | abc | defg | hijk |
        +-----+------+------+
        ''').strip())

    def test_table_with_many_headers_and_rows_missing_some_columns(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'spam': 4567, 'eggs': 8910})
        my_table.rows.append({'ham': 321, 'eggs': 1098})
        my_table.rows.append({'ham': 'abc', 'spam': 'defg'})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        |     | 4567 | 8910 |
        | 321 |      | 1098 |
        | abc | defg |      |
        +-----+------+------+
        ''').strip())

    def test_table_with_changed_separators(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'], dash='=', pipe='-',
                         plus=' ')
        my_table.rows.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.rows.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.rows.append({'ham': 11, 'spam': 22, 'eggs': 33})
        self.assertEqual(str(my_table), dedent('''\
         ===== ====== ====== 
        - ham - spam - eggs -
         ===== ====== ====== 
        -     -      -      -
        -   1 -    2 -    3 -
        -  11 -   22 -   33 -
         ===== ====== ====== '''))

    def test_table_should_accept_rows_as_dict_list_tuple_int_or_float(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 'eggs', 'spam': 'ham', 'eggs': 'spam'})
        my_table.rows.append([1, 42, 3])
        my_table.rows.append([3.14, 2.71, 0.0])
        my_table.rows.append(('spam', 'eggs', 'ham'))
        self.assertEqual(str(my_table), dedent('''
        +------+------+------+
        | ham  | spam | eggs |
        +------+------+------+
        | eggs |  ham | spam |
        |    1 |   42 |    3 |
        | 3.14 | 2.71 |  0.0 |
        | spam | eggs |  ham |
        +------+------+------+
        ''').strip())

    def test_table_should_accept_headers_as_dict_list_tuple_int_or_float(self):
        my_table = Table(headers=[42, 3.14, (4, 2), [3, 14], {'answer': 42}])
        self.assertEqual(str(my_table), dedent('''
        +----+------+--------+---------+----------------+
        | 42 | 3.14 | (4, 2) | [3, 14] | {'answer': 42} |
        +----+------+--------+---------+----------------+
        ''').strip())

    def test_table_with_many_headers_and_rows_right_aligned(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.rows.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.rows.append({'ham': 11, 'spam': 22, 'eggs': 33})
        self.assertEqual(str(my_table), dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        |     |      |      |
        |   1 |    2 |    3 |
        |  11 |   22 |   33 |
        +-----+------+------+
        ''').strip())

    def test_table_with_headers_little_than_rows(self):
        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 'ham spam ham', 'spam': 'spam eggs spam',
                              'eggs': 'eggs ham eggs'})
        self.assertEqual(str(my_table), dedent('''
        +--------------+----------------+---------------+
        |     ham      |      spam      |      eggs     |
        +--------------+----------------+---------------+
        | ham spam ham | spam eggs spam | eggs ham eggs |
        +--------------+----------------+---------------+
        ''').strip())

    def test_output_to_csv_should_create_the_file_correctly_with_headers(self):
        temp_fp = tempfile.NamedTemporaryFile()
        temp_fp.close()

        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': 'ham spam ham', 'spam': 'spam eggs spam',
                              'eggs': 'eggs ham eggs'})
        my_table.to_csv(temp_fp.name)

        fp = open(temp_fp.name)
        contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)

        self.assertEquals(contents, dedent('''\
        "ham","spam","eggs"
        "ham spam ham","spam eggs spam","eggs ham eggs"
        '''))

    def test_should_import_data_from_csv(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.write(dedent('''\
        "ham","spam","eggs"
        "ham spam ham","spam eggs spam","eggs ham eggs"
        "ham spam","eggs spam","eggs eggs"
        '''))
        temp_fp.close()

        my_table = Table(from_csv=temp_fp.name)
        os.remove(temp_fp.name)
        self.assertEquals(str(my_table), dedent('''
        +--------------+----------------+---------------+
        |     ham      |      spam      |      eggs     |
        +--------------+----------------+---------------+
        | ham spam ham | spam eggs spam | eggs ham eggs |
        |     ham spam |      eggs spam |     eggs eggs |
        +--------------+----------------+---------------+
        ''').strip())

    def test_should_save_data_into_text_file(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()

        my_table = Table(headers=['ham', 'spam', 'eggs'])
        my_table.rows.append({'ham': '', 'spam': '', 'eggs': ''})
        my_table.rows.append({'ham': 1, 'spam': 2, 'eggs': 3})
        my_table.rows.append({'ham': 11, 'spam': 22, 'eggs': 33})

        my_table.to_text_file(temp_fp.name)
        fp = open(temp_fp.name, 'r')
        contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)
        self.assertEqual(contents, dedent('''
        +-----+------+------+
        | ham | spam | eggs |
        +-----+------+------+
        |     |      |      |
        |   1 |    2 |    3 |
        |  11 |   22 |   33 |
        +-----+------+------+
        ''').strip())

    def test_character_count_in_row_data_should_use_unicode(self):
        my_table = Table(headers=['First name', 'Last name'])
        my_table.rows.append({'First name': 'Álvaro', 'Last name': 'Justen'})
        my_table.rows.append(['Tatiana', 'Al-Chueyr'])
        my_table.rows.append(('Flávio', 'Amieiro'))
        self.assertEqual(str(my_table), dedent('''
        +------------+-----------+
        | First name | Last name |
        +------------+-----------+
        |     Álvaro |    Justen |
        |    Tatiana | Al-Chueyr |
        |     Flávio |   Amieiro |
        +------------+-----------+
        ''').strip())

    def test_character_count_in_headers_should_be_unicode(self):
        my_table = Table(headers=['ÁÀÃÂÇ', 'ÇÉÈẼÊ'])
        my_table.rows.append(('spam', 'eggs'))
        my_table.rows.append(('eggs', 'spam'))
        self.assertEqual(str(my_table), dedent('''
        +-------+-------+
        | ÁÀÃÂÇ | ÇÉÈẼÊ |
        +-------+-------+
        |  spam |  eggs |
        |  eggs |  spam |
        +-------+-------+
        ''').strip())

    def test_input_and_ouput_character_encoding_in_headers(self):
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        self.assertEqual(str(my_table), dedent('''
        +--------+
        | Álvaro |
        +--------+
        ''').strip().decode('utf8').encode('iso-8859-1'))

    def test_input_and_output_character_encoding_in_method_to_csv(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        my_table.rows.append(['Píton'.decode('utf8').encode('utf16')])
        my_table.to_csv(temp_fp.name)

        fp = open(temp_fp.name)
        file_contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)
        output = '"Álvaro"\n"Píton"\n'.decode('utf8').encode('iso-8859-1')
        self.assertEqual(file_contents, output)

    def test_input_and_output_character_encoding_in_method_to_text_file(self):
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.close()
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        my_table.rows.append(['Píton'.decode('utf8').encode('utf16')])
        my_table.to_text_file(temp_fp.name)

        fp = open(temp_fp.name)
        file_contents = fp.read()
        fp.close()
        os.remove(temp_fp.name)
        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip().decode('utf8').encode('iso-8859-1')
        self.assertEqual(file_contents, output)

    def test_output_character_encoding_in_method___str__(self):
        my_table = Table(headers=['Álvaro'.decode('utf8').encode('utf16')],
                         input_encoding='utf16', output_encoding='iso-8859-1')
        my_table.rows.append(['Píton'.decode('utf8').encode('utf16')])

        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip().decode('utf8').encode('iso-8859-1')
        self.assertEqual(str(my_table), output)

    def test_input_and_output_character_encoding_in_parameter_from_csv(self):
        data = '"Álvaro"\n"Píton"'
        temp_fp = tempfile.NamedTemporaryFile(delete=False)
        temp_fp.write(data.decode('utf8').encode('iso-8859-1'))
        temp_fp.close()
        my_table = Table(from_csv=temp_fp.name, input_encoding='iso-8859-1',
                         output_encoding='utf16')
        os.remove(temp_fp.name)
        output = dedent('''
        +--------+
        | Álvaro |
        +--------+
        |  Píton |
        +--------+
        ''').strip().decode('utf8').encode('utf16')
        self.assertEqual(str(my_table), output)

    def test___unicode__should_return_unicode_no_matter_the_input_encoding(self):
        my_table = Table(headers=['ÁÀÃÂÇ', 'ÇÉÈẼÊ'])
        my_table.rows.append(('spam', 'eggs'))
        my_table.rows.append(('eggs', 'spam'))
        self.assertEqual(unicode(my_table), dedent('''
        +-------+-------+
        | ÁÀÃÂÇ | ÇÉÈẼÊ |
        +-------+-------+
        |  spam |  eggs |
        |  eggs |  spam |
        +-------+-------+
        ''').strip().decode('utf8'))

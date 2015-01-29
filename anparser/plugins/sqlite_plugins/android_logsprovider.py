# -*- coding: utf-8 -*-
"""
anparser - an Open Source Android Artifact Parser
Copyright (C) 2015  Preston Miller

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'prmiller91'
__license__ = 'GPLv3'
__date__ = '20150125'
__version__ = '0.00'

from collections import OrderedDict
import logging
import __init__
import time


def android_logsprovider(file_list):
    """
    Parses logs.db database from com.sec.android.provider.logsprovider

    :param file_list: List of all files
    :return: Dictionary of parsed data from database
    """
    # Initialize table variables: logs
    logs_database = None
    logsprovider_data = None

    for file_path in file_list:
        if file_path.endswith('logs.db') and file_path.count('logsprovider') > 0:
            logs_database = file_path
            try:
                tables = __init__.get_sqlite_table_names(file_path)
            except (IndexError, TypeError) as exception:
                logging.error('SQLite Read Error: {0:s}'.format(file_path + " > " + str(exception)))
                tables = []

            if 'logs' in tables:
                try:
                    logsprovider_data = __init__.read_sqlite_table(
                        file_path, 'logs',
                        columns='_id, number, address, date, duration, type, new, name, is_read, '
                                'countryiso, geocoded_location, normalized_number, messageid, contactid, '
                                'm_subject, m_content, account_name, account_id, fname, lname, country_code, cityid')
                except __init__.sqlite3.OperationalError as exception:
                    logging.error('Sqlite3 Operational Error: {0:s}'.format(exception))
                    pass

    logs_data_list = []
    logs_data = OrderedDict()

    # Add data from logs.db to logs_data_list
    # Add data from logs table to logs_data
    if logsprovider_data:
        for entry in logsprovider_data:
            logs_data['Database'] = logs_database
            logs_data['Table'] = 'logs'
            logs_data['Log Id'] = entry[0]
            logs_data['Account Id'] = entry[17]
            logs_data['Message Id'] = entry[12]
            logs_data['Contact Id'] = entry[13]
            logs_data['Account Name'] = entry[16]
            logs_data['F Name'] = entry[18]
            logs_data['L Name'] = entry[19]
            logs_data['Name'] = entry[7]
            logs_data['Number'] = entry[1]
            logs_data['Normalized Number'] = entry[11]
            logs_data['M Subject'] = entry[14]
            logs_data['M Content'] = entry[15]
            logs_data['Duration'] = entry[4]
            try:
                logs_data['Date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(entry[3] / 1000.))
            except TypeError:
                logs_data['Date'] = ''
            logs_data['Address'] = entry[2]
            logs_data['Country Iso'] = entry[9]
            logs_data['Geocoded Location'] = entry[10]
            logs_data['City Id'] = entry[21]
            logs_data['Country Code'] = entry[20]
            logs_data['Type'] = entry[5]
            logs_data['New'] = entry[6]
            logs_data['Is Read'] = entry[8]

            logs_data_list.append(logs_data)
            logs_data = OrderedDict()

    return logs_data_list
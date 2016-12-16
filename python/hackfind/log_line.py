#  log_line.py - Handles parsing a single log line.
#
# Copyright (C) 2016 Darryl L. Pierce <mcpierce@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re, time
from datetime import datetime

class LogLine:
    IP_RE = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    DEF_TIMESTAMP = re.compile("(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (.+) (.+) (.+) (.+) (.+) \(PST\)$")
    ACCESS_ATTEMPT_WITH_DT = re.compile("\[LAN access from remote] from (%s):\d+ to (%s):(\d+), (Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday), (.*)" % (IP_RE, IP_RE))
    ACCESS_ATTEMPT = re.compile("\[LAN access from remote] from (%s):(\d{1,5})" % IP_RE)


    def __init__(self, model, line):
        self.__model = model
        self.__line = line.strip("\r\n")
        self.__parse_line_and_extract_details()

    @staticmethod
    def process(line, model):
        """
        Processes a single line and, if it contains an entry, extracts it
        and modifies the specified model.
        """
        o = LogLine(model, line)
        

    def __parse_line_and_extract_details(self):
        if not self.__is_default_timestamp():
            if not self.__is_access_attempt():
                # useless line
                pass

    def __is_default_timestamp(self):
        if LogLine.DEF_TIMESTAMP.search(self.__line):
            match = self.DEF_TIMESTAMP.search(self.__line)
            line = "%s %s %s %s" % (match.group(2), match.group(3), match.group(4), match.group(5))
            self.__model.default_timestamp = time.mktime(datetime.strptime(line, "%d %b %Y %H:%M:%S").timetuple())
            return True
        else:
            return False

    def __is_access_attempt(self):
        if LogLine.ACCESS_ATTEMPT.search(self.__line):
            if LogLine.ACCESS_ATTEMPT_WITH_DT.search(self.__line):
                match = LogLine.ACCESS_ATTEMPT_WITH_DT.search(self.__line)
                source = match.group(1)
                port = int(match.group(3))
                when = time.mktime(datetime.strptime(match.group(5), "%B %d, %Y %H:%M:%S").timetuple())
                self.__add_attempt_to_model(source, port, when)
                return True
            elif LogLine.ACCESS_ATTEMPT.search(self.__line):
                match = LogLine.ACCESS_ATTEMPT.search(self.__line)
                source = match.group(1)
                port = int(match.group(2))
                self.__add_attempt_to_model(source, port)
                return True
            else:
                return False
        else:
            return False

    def __add_attempt_to_model(self, source, port, when = None):
        if when is None: when = self.__model.default_timestamp
        # if there is a time range then honor it
        if self.__model.earliest_date is not None and when < self.__model.earliest_date:
            return
        if self.__model.latest_date is not None and when > self.__model.latest_date:
            return
        self.__model.add_access_attempt(source, port, when)
            

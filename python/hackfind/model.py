# model.py - holds the data model for the log files
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

from log_line import LogLine
from access_attempt import AccessAttempt
from access_totals import AccessTotals
from address import Address
from address_block import AddressBlock

class Model:
    """Holds a reference to the details of a set of log file."""

    def __init__(self, ifile):
        """
        Create a new instance based on the contents of the supplied file.
        """
        self._ifile = ifile
        self.__countries = {}
        self.__included_ports = []
        self.__ignored_ports = []
        self.__access_totals = AccessTotals()
        self.__earliest_date = None
        self.__latest_date = None

    @property
    def earliest_date(self):
        return self.__earliest_date

    @earliest_date.setter
    def earliest_date(self, time):
        self.__earliest_date = time

    @property
    def latest_date(self):
        return self.__latest_date

    @latest_date.setter
    def latest_date(self, time):
        self.__latest_date = time

    @property
    def country_names(self):
        return self.__countries.keys()

    @property
    def sorted_countries(self):
         return sorted(self.__countries.values(), key=lambda c: c.name)

    @property
    def total_attempts(self):
        return sum(country.total_attempts for country in self.__countries.values())

    @property
    def totals_by_date(self):
        return self.__access_totals.get_totals_by_date()

    @property
    def total_addresses(self):
        return sum(country.total_addresses for country in self.__countries.values())

    def attack_ratio_for_country(self, country):
        return float(country.total_attempts) / float(self.total_attempts)

    def get_country(self, name):
        return self.__countries[name]

    def set_included_ports(self, ports):
        self.__included_ports = ports

    def process_input(self):
        """
        Begins processing the input file, extracting the desired access
        attempt entries and building the document model.
        """
        with open(self._ifile) as f:
            lines = f.readlines()
            for line in lines:
                LogLine.process(line, self)

    def add_access_attempt(self, source, port, when):
        """
        Tracks a new attempt at accessing the network.
        """
        # only process ports we're tracking
        if port in self.__included_ports:
            address = Address.for_source(source)
            if not self.__countries.has_key(address.country.name):
                self.__countries[address.country.name] = address.country
            if address.add_attempt(when, port):
                self.__access_totals.add_attempt(when, port)
        elif port not in self.__ignored_ports:
            self.__ignored_ports.append(port)

    def get_default_timestamp(self):
        return self.__default_timestamp

    def set_default_timestamp(self, timestamp):
        self.__default_timestamp = timestamp

    timestamp = property(get_default_timestamp, set_default_timestamp)

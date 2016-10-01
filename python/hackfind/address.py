# address.py
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

class Address:
    """Represents a single IP address."""

    __instances = {}

    def __init__(self, address):
        self.__address = address
        self.__attempts_by_port = {}
        self.__attempts = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s (attempts=%d)" % (self.__address, len(self.__attempts))

    @classmethod
    def for_source(cls, address):
        """
        Returns an instance for the specified class. If no such instance
        exists then it creates a new one and returns it.
        """
        if cls.__instances.has_key(address):
            result = cls.__instances[address]
        else:
            result = Address(address)
            cls.__instances[address] = result
        return result

    def add_attempt(self, date, port):
        self.__attempts.append(date)
        if self.__attempts_by_port.has_key(port):
            attempts = self.__attempts_by_port[port]
        else:
            attempts = []
            self.__attempts_by_port[port] = attempts
        attempts.append(date)

    @property
    def address(self):
        return self.__address

    @property
    def attempts(self):
        return self.__attempts

    @property
    def oldest_attempt(self):
        return sorted(self.__attempts)[0]

    @property
    def newest_attempt(self):
        return sorted(self.__attempts)[-1]

    @property
    def total_attempts(self):
        return len(self.__attempts)

    @property
    def attempts_sorted_by_date(self):
        return sorted(self.__attempts, key=lambda attempt: attempt[0])

    @classmethod
    def overall_oldest_attempt(cls):
        result = None
        for address in cls.__instances:
            if result is None or address.oldest_attempt[0] < result:
                result = address.oldest_attempt[0]
        return result

    @classmethod
    def overall_newest_attempt(cls):
        result = None
        for address in cls.__instances:
            if result is None or address.newest_attempt[0] > result:
                result = address.newest_attempt[0]
        return result

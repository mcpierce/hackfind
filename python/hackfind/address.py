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

    __instances = []

    def __init__(self, address):
        self.__address = address
        self.__attempts = [] # (date, port)
        Address.__instances.append(self)

    def add_attempt(self, date, port):
        self.__attempts.append([date, port])

    @property
    def address_block(self):
        return self.__address[:self.__address.rfind(".")]

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

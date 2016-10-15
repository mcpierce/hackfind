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

from country import Country

import GeoIP

class Address:
    """Represents a single IP address."""

    GI = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

    __instances = {}

    def __init__(self, address):
        self.__address = address
        self.__attempts_by_port = {}
        self.__country = Country.for_name(Address.GI.country_name_by_addr(address))
        self.__country.add_address(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__address

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
    def country(self):
        return self.__country

    @property
    def ports_targeted(self):
        return self.__attempts_by_port.keys()

    def attempts_for_port(self, port):
        return self.__attempts_by_port[port]

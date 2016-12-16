# country.py
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

from address_block import AddressBlock

class Country:
    """Represents a single country."""

    __instances = []
    __by_name = {}

    def __init__(self, name):
        self.__name = name
        self.__address_block = AddressBlock()
        # keep track of all instances
        Country.__instances.append(self)
        Country.__by_name[name] = self

    def add_address(self, address):
        self.__address_block.add_address(address)

    @property
    def total_addresses(self):
        return self.__address_block.total_addresses

    @property
    def sorted_addresses(self):
        return self.__address_block.sorted_addresses

    def remove_address(self, address):
        self.__address_block.remove_address(address)

    @property
    def sorted_networks(self):
        return self.__address_block.sorted_networks

    def sorted_addresses_for_network(self, network):
        return self.__address_block.sorted_addresses_for_network(network)

    def total_attempts_for_network(self, network):
        return self.__address_block.total_attempts_for_network(network)

    @property
    def total_attempts(self):
        return self.__address_block.total_attempts

    def total_for_date(self, date):
        return self.__address_block.total_attempts_for_date(date)

    @property
    def name(self):
        return self.__name if self.__name is not None else "Indeterminate"

    @property
    def address_block(self):
        return self.__address_block.root

    def _find_access_date(self, oldest):
        result = None
        for address in self.__addresses.values():
            if oldest:
                if result is None or address.oldest_attempt < result:
                    result = address.oldest_attempt
            else:
                if result is None or address.newest_attempt > result:
                    result = address.newest_attempt
        return result[0]

    @classmethod
    def for_name(cls, name):
        if not cls.__by_name.has_key(name):
            cls.__by_name[name] = Country(name)
        return cls.__by_name.get(name)

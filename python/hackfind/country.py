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

class Country:
    """Represents a single country."""

    __instances = []
    __by_name = {}

    def __init__(self, name):
        self.__name = name
        self.__addresses = {}
        self.__by_block = {}
        # keep track of all instances
        Country.__instances.append(self)
        Country.__by_name[name] = self

    def add_address(self, address):
        self.__addresses[address.address] = address
        block = self.__by_block.get(address.address_block)
        if block is None:
            block = {}
            self.__by_block[address.address_block] = block
        block[address.address] = address

    @property
    def name(self):
        return self.__name if self.__name is not None else "Indeterminate"

    @property
    def raw_name(self):
        return self.__name

    @property
    def total_addresses(self):
        return len(self.__addresses)

    @property
    def total_address_blocks(self):
        return len(self.__by_block.keys())

    @property
    def address_blocks(self):
        return self.__by_block

    def for_address(self, address):
        return self.__addresses.get(address)

    @property
    def addresses(self):
        return self.__addresses

    @property
    def sorted_addresses(self):
        return sorted(self.__addresses.values(), key = lambda a: a.address)

    @property
    def oldest_attempt(self):
        return self._find_access_date(oldest = True)

    @property
    def newest_attempt(self):
        return self._find_access_date(oldest = False)

    @property
    def total_attempts(self):
        return reduce(lambda x, y: x + y.total_attempts, self.__addresses.values(), 0)

    @property
    def attack_ratio(self):
        return float(self.total_attempts) / float(self.total_addresses)

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
    def get_top_offenders(cls, size=5):
        """Returns the top offenders, up to size in number."""
        return sorted(cls.__instances, key = lambda a: a.total_attempts, reverse=True)[:size]

    @classmethod
    def get_instances(cls):
        return cls.__instances

    @classmethod
    def for_name(cls, name):
        return cls.__by_name.get(name)

    @classmethod
    def by_name(cls):
        return sorted(cls.__instances, key = lambda a: a.name)

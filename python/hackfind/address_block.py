# address_block.py
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

class AddressBlock:
    """
    An AddressBlock maintains a hierarchy of addresses based on segments.
    """

    def __init__(self):
        self.__root = {}
        self.__all = []
        self.__networks = {}

    @property
    def root(self):
        return self.__root

    def add_address(self, address):
        # if we're not already processed the address, then process
        if address not in self.__all:
            self.__all.append(address)
            # break down the address and add it to the tree
            one, two, three, four = address.address.split(".")
            self.__piecewise_add(address, one, two, three, four)

    @property
    def total_addresses(self):
        return len(self.__all)

    @property
    def sorted_addresses(self):
        return sorted(self.__all)

    @property
    def sorted_networks(self):
        return sorted(self.__networks.keys())

    def sorted_addresses_for_network(self, network):
        return sorted(self.__networks[network])

    @property
    def total_attempts(self):
        return sum(addr.total_attempts for addr in self.__all)

    def total_attempts_for_network(self, network):
        return sum(addr.total_attempts for addr in self.sorted_addresses_for_network(network))

    def total_attempts_for_date(self, date):
        return sum(addr.total_attempts_for_date(date) for addr in self.__all)

    def remove_address(self, address):
        if address in self.__all:
            self.__all.remove(address)
            # iterate through all 

    def __piecewise_add(self, address, one, two, three, four):
        top_key = "%s.%s" % (one, two)
        network_key = "%s.%s.%s" % (one, two, three)

        if self.__root.has_key(top_key):
            top = self.__root[top_key]
        else:
            top = {}
            self.__root[top_key] = top

        if self.__networks.has_key(network_key):
            block = self.__networks[network_key]
        else:
            block = []
            self.__networks[network_key] = block
            if address not in block: block.append(address)

        if top.has_key(three):
            bottom = top[three]
        else:
            bottom = []
            top[three] = bottom

        if address not in bottom:
            bottom.append(address)

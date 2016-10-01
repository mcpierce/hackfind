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

    @property
    def root(self):
        return self.__root

    def add_address(self, address):
        # if we're not already processed the address, then process
        if address not in self.__all:
            self.__all.append(address)
            # break down the address and add it to the tree
            one, two, three, four = address.address.split(".")
            self.__piecewise_add(address, one, two, three)

    def __piecewise_add(self, address, one, two, three):
        if self.__root.has_key(one):
            first = self.__root[one]
        else:
            first = {}
            self.__root[one] = first

        if first.has_key(two):
            second = first[two]
        else:
            second = {}
            first[two] = second

        if second.has_key(three):
            third = second[three]
        else:
            third = []
            second[three] = third

        if address not in third:
            third.append(address)

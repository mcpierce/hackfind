# report.py
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

import sys

from utils import get_timestamp

class Report:
    def __init__(self, ofile):
        self.__ofile = ofile
        self.__old_stdout = None

    def write_output(self, model):
        # if an output file was specified, then redirect stdout to it
        try:
            if len(self.__ofile) > 0:
                print("Writing to %s" % self.__ofile)
                self.__old_stdout = sys.stdout
                sys.stdout = open(self.__ofile, "w")

                self.__generate_report_body(model)

        finally:
            if self.__old_stdout is not None:
                sys.stdout = self.__old_stdout
                self.__old_stdout = None

    def __create_line(self, address, port, when):
        return "%-15s %5s %s" % (address, port, get_timestamp(when))

    def __generate_report_body(self, model):
        # iterate through all the entries in our model and add
        # entries to the report created
        for country_name in sorted(model.country_names):
            country = model.get_country(country_name)
            print("Country: %s" % country.name)
            total_addresses = 0
            total_attacks = 0
            for top_level_key in sorted(country.address_block):
                top_level = country.address_block[top_level_key]
                for bottom_key in sorted(top_level.iterkeys()):
                    bottom = top_level[bottom_key]
                    print("")
                    print("Network block: %s.%s.*" % (top_level_key, bottom_key))
                    print("")
                    print("    ADDRESS      PORT      DATE/TIME          ADDRESS      PORT      DATE/TIME")
                    print("=============== ===== =================== =============== ===== ===================")
                    for address in bottom:
                        total_addresses = total_addresses + 1
                        total_attacks = total_attacks + address.number_of_attempts
                        rows = (len(address.attempts) + 1) / 2
                        attempts = address.attempts_sorted_by_date
                        for row in range(0, rows):
                            output = self.__create_line(address.address, attempts[row].port, attempts[row].when)
                            if (row + rows) < len(address.attempts):
                                output = "%s %s" % (output,
                                                    self.__create_line(address.address,
                                                                       attempts[row + rows].port,
                                                                       attempts[row + rows].when))
                            print(output)
            print("===================================================================================")
            print("Statistics for %s:" % country.name)
            print("    Total addresses...: %d" % total_addresses)
            print("    Total attempts....: %d" % total_attacks)
            print("    Attack ratio......: %.3f" % (float(total_attacks) / float(total_addresses)))
            print("")


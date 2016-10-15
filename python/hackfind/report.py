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
            for one_key in sorted(country.address_block):
                one = country.address_block[one_key]
                for two_key in sorted(one.iterkeys()):
                    two = one[two_key]
                    print("")
                    print("         Address block: %s.%s.*.*" % (one_key, two_key))
                    for three_key in sorted(two.iterkeys()):
                        three = two[three_key]
                        for four_key in sorted(three.iterkeys()):
                            four = three[four_key]
                            print("    ADDRESS      PORT      DATE/TIME          ADDRESS      PORT      DATE/TIME")
                            print("=============== ===== =================== =============== ===== ===================")
                            for address in four:
                                total_addresses = total_addresses + 1
                                for port in sorted(address.ports_targeted):
                                    attempts = address.attempts_for_port(port)
                                    total_attacks = total_attacks + len(attempts)
                                    rows = (len(attempts) + 1) / 2
                                    for row in range(0, rows):
                                        line = self.__create_line(address.address,
                                                                  port,
                                                                  attempts[row])
                                        if (row + rows) < len(attempts):
                                            line = "%s %s" % (line,
                                                              self.__create_line(address.address,
                                                                                 port,
                                                                                 attempts[row + rows]))
                                        print(line)
                                        print("===================================================================================")
                                        print("Statistics for %s:" % country.name)
                                        print("    Total addresses...: %d" % total_addresses)
                                        print("    Total attempts....: %d" % total_attacks)
                                        print("    Attack ratio......: %.3f" % (float(total_attacks) / float(total_addresses)))
                                        print("")


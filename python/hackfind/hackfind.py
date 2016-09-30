# hackfind.py
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

from __future__ import print_function

import sys

from address import Address
from country import Country

import time
from datetime import datetime
import socket
import re
import GeoIP

GI = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
TOTALS = {}

IP_RE = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
default_timestamp_re = re.compile("(Sun|Mon|Tue|Wed|Thu|Fri|Sat), (.+) (.+) (.+) (.+) (.+) \(PST\)$")
access_attempt_re = re.compile("\[LAN access from remote] from (%s):(\d{1,5})" % IP_RE)
access_attempt_with_datetime_re = re.compile("\[LAN access from remote] from (%s):\d+ to (%s):(\d+), (Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday), (.*)" % (IP_RE, IP_RE))

default_datetime = ""

def get_timestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime("%m/%d/%Y %H:%M:%S")

def get_datestamp(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime("%m/%d/%Y")

def get_month_and_year(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime("%m/%Y")

def get_number_of_days(newest, oldest):
    return (datetime.utcfromtimestamp(newest) - datetime.utcfromtimestamp(oldest)).days + 1

def show_output(text):
    print("%s | %s" % (get_timestamp(time.time()), text))

def convert_month_first(timestamp):
    return time.mktime(datetime.strptime(timestamp, "%B %d, %Y %H:%M:%S").timetuple())

def get_default_datetime(line):
    # match = re.search(DEFAULT_TIMESTAMP_RE, line)
    match = default_timestamp_re.search(line)
    global default_datetime
    line = "%s %s %s %s" % (match.group(2), match.group(3), match.group(4), match.group(5))
    default_datetime = time.mktime(datetime.strptime(line, "%d %b %Y %H:%M:%S").timetuple())

def store_access_detail(geoip, source, port, when, totals=False):
    # get the country's details, then get the source IP address's details
    country = Country.for_name(geoip)
    if country is None:
        country = Country(geoip)
    address = country.for_address(source)
    if address is None:
        address = Address(source)
        country.add_address(address)
    address.add_attempt(when, port)

    # if we're doing totals, then add them
    if totals:
        date = get_month_and_year(when)
        record = TOTALS.get(date)
        if record is None:
            record = 0
            TOTALS[date] = record
        record = record + 1
        TOTALS[date] = record

def get_access_source(line, totals=False):
    # first see if we have a datetime entry
    match = access_attempt_with_datetime_re.search(line)
    if match:
        source = match.group(1)
        port = int(match.group(3))
        when = convert_month_first(match.group(5))
    else:
        match = access_attempt_re.search(line)
        source = match.group(1)
        port = int(match.group(2))
        when = default_datetime

    # get the geoip information for the source
    geoip = GI.country_name_by_addr(source)
    store_access_detail(geoip, source, port, when, totals)

def process_line(line, totals=False):
    line = line.strip("\r\n")
    # if the line contains "(PST)" then it has a default date stamp
    # if re.search(DEFAULT_TIMESTAMP_RE, line):
    if default_timestamp_re.search(line):
        get_default_datetime(line)
    elif access_attempt_re.search(line):
        get_access_source(line, totals)

def update_top_offenders(top_offenders_list, count, country):
    # find a country with fewer offenses and insert the supplied country
    index = 0
    while top_offenders_list[index] is not None and top_offenders_list[index][0] >= count and index < len(top_offenders_list):
        print("Updating %d for %s (%d)" % (index, country, count))
        index = index + 1
    if index < len(top_offenders_list):
        current = len(top_offenders_list) - 1
        while current > index and current > 1:
            top_offenders_list[current] = top_offenders_list[current - 1]
            current = current - 1
        print("Inserting %s at %d" % (country, index))
        top_offenders_list[index] = [count, country]

def lookup_hostname(address):
    try:
        return socket.gethostbyaddr(address)[1]
    except socket.herror:
        return "Unknown"
      
def generate_full_access_report(group_addresses, hostnames):
    longest_running_attempts = [0, None, None, None, None]
  
    for country in Country.by_name():
        print("COUNTRY: %s" % country.name)
        print("         Total addresses........: %d" % country.total_addresses)
        print("         Total attempts.........: %d" % country.total_attempts)
        if group_addresses and country.total_address_blocks > 1:
            print("")
            print("Total address blocks...: %d" % country.total_address_blocks)
            print("   BLOCK     # ADDR  # HITS")
            print("===========  ======  ======")
            for block in country.address_blocks.keys():
                total_attempts = 0
                for address in country.address_blocks[block].values():
                    total_attempts = total_attempts + address.total_attempts
                print("%11s  %6d  %6d" %(block,
                                         len(country.address_blocks[block].values()),
                                         total_attempts))
        print("")
        for address in sorted(country.sorted_addresses):
            address_oldest = address.oldest_attempt
            address_newest = address.newest_attempt
            if get_number_of_days(address_newest[0], address_oldest[0]) > longest_running_attempts[0]:
                longest_running_attempts = (get_number_of_days(address_newest[0], address_oldest[0]),
                                            address.total_attempts, address, country,
                                            get_datestamp(address_oldest[0]),
                                            get_datestamp(address_newest[0]))
            print("")
            print("IP ADDRESS: %s [%d attempt(s)] from %s to %s" % (address.address, address.total_attempts, get_datestamp(address_oldest[0]), get_datestamp(address_newest[0])))
            if hostnames: print("  HOSTNAME: %s" % lookup_hostname(address.address))
            print("  DATE OF ACCESS    PORT#    DATE OF ACCESS    PORT#    DATE OF ACCESS    PORT#")
            print("=================== =====  =================== =====  =================== =====")
            which = 0
            for attempt in sorted(address.attempts):
                if which in [1, 2]:
                    print("  ", end='')
                print("%19s %5d" % (get_timestamp(attempt[0]), attempt[1]), end='')
                which = which + 1
                if which is 3:
                    print("")
                    which = 0
            print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
    print("===== Top %d offending countries (by access attempts)" % len(Country.get_top_offenders()))
    for offender in Country.get_top_offenders():
        if offender is not None:
            print("      %40s: %5d attempts   %3d addresses   Ratio=%0.3f)" % (offender.name, offender.total_attempts, offender.total_addresses, offender.attack_ratio))
    print("")

def generate_totals_report(ofile, totals_only, group_addresses, hostnames):
    old_stdout = sys.stdout
    if len(ofile) > 0:
        show_output("Writing to %s" % ofile)
        sys.stdout = open(ofile, "w")

    if not totals_only:
        generate_full_access_report(group_addresses, hostnames)

    print("Country totals from %s to %s" % (get_datestamp(Address.overall_oldest_attempt()),
                                            get_datestamp(Address.overall_newest_attempt())))
    print("                  COUNTRY                 ADDRS  TOTAL    OLDEST      NEWEST    # DAYS")
    print("========================================  =====  =====  ==========  ==========  ======")
    for country in sorted(Country.get_instances(), key = lambda x: x.raw_name):
        print("%-40s  %5d  %5d  %s  %s  %6s" % (country.name, country.total_addresses, country.total_attempts, get_datestamp(country.oldest_attempt), get_datestamp(country.newest_attempt), get_number_of_days(country.newest_attempt, country.oldest_attempt)))

    if len(ofile) > 0:
        sys.stdout.close()
        sys.stdout = old_stdout

def generate_cvs_report():
    show_output("Writing CSV file: %s" % cfile)

    old_stdout = sys.stdout
    sys.stdout = open(cfile, "w")
    print("\"DATE\",\"COUNTRY\",\"IP ADDRESS\"")
    for country in Country.by_name():
        for address in country.sorted_addresses:
            for detail in address.attempts_sorted_by_date:
                print("\"%s\",\"%s\",\"%s\"" % (get_timestamp(detail[0]), country, address))
    sys.stdout.close()
    sys.stdout = old_stdout

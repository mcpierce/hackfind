# access_attempt.py
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

from utils import get_timestamp

class AccessAttempt:
    def __init__(self, port, when):
        self.__port = port
        self.__when = when

    @property
    def port(self):
        return self.__port

    @property
    def when(self):
        return self.__when

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "Access attempt: port %d on %s" % (self.__port, get_timestamp(self.__when))

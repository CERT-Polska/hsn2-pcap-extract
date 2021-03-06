# Copyright (c) NASK
#
# This file is part of HoneySpider Network 2.1.
#
# This is a free software: you can redistribute it and/or modify
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

from hsn2_pcap_extract.verifiers.VerifierAbstract import VerifierAbstract


class VerifierMimetester(VerifierAbstract):

    def __init__(self):
        pass

    def verify(self, filepath, mimetype, extension, config):
        mimeList = config.get("mimetype", extension)
        arr = mimeList.split(",")
        return mimetype in arr

    def getName(self):
        return "Mimetester verifier"

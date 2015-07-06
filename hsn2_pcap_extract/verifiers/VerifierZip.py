# Copyright (c) NASK
#
# This file is part of HoneySpider Network 2.0.
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

import re
from hsn2_pcap_extract.verifiers.VerifierAbstract import VerifierAbstract
from hsn2_pcap_extract.external import External


class VerifierZip(VerifierAbstract):

    def verify(self, filepath, mimetype, extension, config):
        external = External()
        output = external.runExternal(["zip", "--test", filepath])
        if re.match("(.*)OK(.*)", output[0], re.I) is not None:
            return True
        return False

    def getName(self):
        return "Zip verifier"

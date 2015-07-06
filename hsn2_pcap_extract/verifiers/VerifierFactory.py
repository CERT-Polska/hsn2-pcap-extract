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

import ConfigParser
from hsn2_pcap_extract.verifiers.VerifierZip import VerifierZip
from hsn2_pcap_extract.verifiers.VerifierPefile import VerifierPefile
from hsn2_pcap_extract.verifiers.VerifierMimetester import VerifierMimetester


class VerifierFactory():

    verifiersLists = None

    def __init__(self):
        self.verifiersLists = {}

    def getVerifier(self, name):
        if name == "zip":
            return VerifierZip()
        if name == "pefile":
            return VerifierPefile()
        if name == "mimetester":
            return VerifierMimetester()

    def createVerifierList(self, configValue):
        arr = configValue.split(",")
        tmpDict = []
        for verifier in arr:
            tmpDict.append(self.getVerifier(verifier))
        return tmpDict

    def getVerifierList(self, fileExtension, config):
        try:
            return self.verifiersLists[fileExtension]
        except KeyError:
            try:
                configValue = config.get("verifier", fileExtension)
                self.verifiersLists[fileExtension] = self.createVerifierList(configValue)
                return self.verifiersLists[fileExtension]
            except ConfigParser.NoOptionError:
                return self.getVerifierList("default", config)

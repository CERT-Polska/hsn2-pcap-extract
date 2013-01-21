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

'''
Created on Jul 12, 2012

@author: pawelb
'''

class VerifierAbstract():

	def __init__(self):
		raise NotImplementedError("Can't create an instance of VerifierAbstract")
	
	def verify(self, filepath, mimetype, extension, config):
		raise NotImplementedError("Method verify isn't implemented")
	
	def getName(self):
		raise NotImplementedError("Method getName isn't implemented")

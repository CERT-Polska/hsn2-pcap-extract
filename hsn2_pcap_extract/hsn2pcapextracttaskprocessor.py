#!/usr/bin/python -tt

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
Created on 10-07-2012

@author: pawelb
'''

import sys
sys.path.append("/opt/hsn2/python/commlib")
from hsn2taskprocessor import HSN2TaskProcessor
from hsn2taskprocessor import ParamException
from hsn2_pcap_extract.verifiers.VerifierFactory import VerifierFactory
from config import Config
from hsn2osadapter import ObjectStoreException

from hsn2objectwrapper import Object

from external import External
import logging
import os
import uuid
import magic


class PcapExtractTaskProcessor(HSN2TaskProcessor):
	parser = None
		
	def __init__(self, connector, datastore, serviceName, serviceQueue, objectStoreQueue, **extra):
	   HSN2TaskProcessor.__init__(self, connector, datastore, serviceName, serviceQueue, objectStoreQueue, **extra)

	def getPcapFilePath(self):
		return self.dsAdapter.saveTmp(self.currentTask.job, self.objects[0].pcap_content.getKey())

	def createNewObject(self, filepath, fileExtension):
		logging.info("Creating new object for file %s" % filepath)

		obj = Object()
		obj.addBytes("content", long(self.dsAdapter.putFile(filepath, self.currentTask.job)))
		obj.addString("file_type", fileExtension)
		return obj

	def taskProcess(self):
		logging.debug(self.__class__)
		logging.debug(self.currentTask)
		logging.debug(self.objects)
		
		jobId = self.currentTask.job
		taskId = self.currentTask.task_id
		external = External()
		
		if len(self.objects) == 0:
			raise ObjectStoreException("Task processing didn't find task object.")
		
		if not self.objects[0].isSet("pcap_content"):
			raise ParamException("pcap_content param is missing.")
		
		outputDir = "/tmp/%s" % uuid.uuid4()
		config = Config().getConfig()
		
		external.runExternal(["mkdir", "-p", outputDir]);
		pcapFilePath = self.getPcapFilePath()
		external.runExternal(["tcpxtract", "-f", pcapFilePath, "-o", outputDir]);
		
		dirList=os.listdir(outputDir)
		verifierFactory = VerifierFactory()
		objects = list()
		for fname in dirList:
			filepath = "%s/%s" % (outputDir, fname)
			m = magic.open(magic.MAGIC_MIME)
			m.load()
			result = m.file(filepath)
			mimetype = result.split(";")[0]
			
			_, fileExtension = os.path.splitext(filepath)
			fileExtension = fileExtension[1:]
			
			verifierList = verifierFactory.getVerifierList(fileExtension, config)
			result = True;
			for ver in verifierList:
				logging.info("%s, %s, %s" % (filepath, mimetype, fileExtension))
				result = result and ver.verify(filepath, mimetype, fileExtension, config)
				if not result:
					break
				
			if result:
				objects.append(self.createNewObject(filepath, fileExtension))			
				
		if len(objects) > 0:
			newObjIds = self.osAdapter.objectsPut(jobId, taskId, objects)
			self.newObjects.extend(newObjIds)   
				
		external.runExternal(["rm", "-rf", outputDir, pcapFilePath]);
		return []

if __name__ == '__main__':
	a = PcapExtractTaskProcessor()

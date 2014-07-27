# -*- coding: utf-8 -*-
'''
Author: Berlin
E-Mail: bolinsun@163.com
'''
from threading import Thread
from datetime import datetime
import os, sys
import foreRequester, areaParser

def fileMerger(loc, stime, threadNumber = 20):
	filename = os.path.join(loc, 'gn_360_' + stime + '.txt');
	fw = open(filename, 'wb');
	for i in range(threadNumber):
		fname = 'gn_360_' + stime + '.part.' + str(i);
		if not os.path.exists(fname):
			print 'Failed to find the part file' + fname;
			break;
		fr = open(fname, 'rb');
		data = fr.read();
		fr.close();
		os.remove(fname);
		fw.write(data);
		fw.flush();

	fw.close()

class WeatherJob(Thread):
	def __init__(self, index, area_dict, begin, end, stime):
		Thread.__init__(self)
		self.index = index
		self.stime = stime
		self.area_dict = area_dict
		self.begin = begin
		self.end = end

	def run(self):
		foreRequester.getWeatherInfo(self.index, self.area_dict, self.begin, self.end, self.stime)

def main(loc):
	# If datetime.strptime is used before starting the threads, then no exception is raised.
	stime = datetime.now().strftime('%Y%m%d%H%M%S');
	datetime.strptime("2014-02-22", "%Y-%m-%d");
	area_dict = areaParser.getAreaDict();

	threads = [];
	blockSize = len(area_dict)/20;
	for i in range(19):
		beginPoint = blockSize * i;
		threads.append(WeatherJob(i, area_dict, beginPoint, beginPoint + blockSize, stime));

	assigned = blockSize * 19;
	threads.append(WeatherJob(19, area_dict, assigned, len(area_dict), stime));
	for thread in threads:
		thread.start();
	for thread in threads:
		thread.join();

	fileMerger(loc, stime);

if __name__ == '__main__':
	if len(sys.argv) <> 2:
		print "Usage: forecast3d location"
		sys.exit(1);
	else:
		main(sys.argv[1]);


import sched, time
from threading import Thread, Timer
import subprocess
import sys

s = sched.scheduler(time.time, time.sleep)

class Job(Thread):
	def __init__(self, loc):
		Thread.__init__(self)
		self.loc = loc

	def run(self):
		print_time()
		print '--------------- begin to get weather info ---------------'
		subprocess.call("forecast3d.exe " + self.loc)
		print '---------------  end to get weather info  ---------------'

def each_day_time(hour, min, sec, next_day):
	struct = time.localtime()
	if next_day == 0:
		day = struct.tm_mday + 1
	else:
		day = struct.tm_mday
	return time.mktime((struct.tm_year,struct.tm_mon,day,
	hour,min,sec,struct.tm_wday, struct.tm_yday,
	struct.tm_isdst))

def print_time():
	print "From print_time", time.ctime()

def do_somthing(loc):
	job = Job(loc)
	job.start()

def echo_start_msg():
	print '**************** auto task begin running ****************'

def main(loc, istomorrow=1):
	print '-------------- scheduled task will run once every two hours --------------'
	s.enterabs(each_day_time(8, 0, 0, istomorrow), 1, echo_start_msg, ())
	s.run()
	while(True):
		Timer(0, do_somthing, (loc,)).start()
		time.sleep(3 * 60 * 60)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'Usage: taskSched location <istomorrow>'
		sys.exit()
	elif len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		main(sys.argv[1], sys.argv[2])

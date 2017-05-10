import os
import time
import subprocess
import psutil
import datetime

CORE_COUNT = psutil.cpu_count() # The number of cores available on my machine. Based on this stackoverflow answer: http://stackoverflow.com/questions/1715580/how-to-discover-number-of-logical-cores-on-mac-os-x
AVG_LOAD_THRESHOLD = 1 
LOAD_DURATION_TO_CHECK = 2 # in minuets

class UptimeStatus(object):
	""" Object used to facilitate interacting with the "uptime" shell command and the data points we care about."""
	
	def __init__(self, id=1):
		self.id 		   = id
		self.creation_time = self.set_init_time()
		self.raw_uptime    = subprocess.check_output("uptime", shell=True) # Worth keeping in case we need to debug.
		self.alert_triggered = False
		self.set_load_averages()

	def __repr__(self):
		return "id={id}, creation_time={dt}, load_avg_1min={load_avg_1min}".format(id=self.id, dt=self.creation_time, load_avg_1min=self.load_avg_1min)

	def __str__(self):
		return "id={id}, creation_time={dt}, load_avg_1min={load_avg_1min}".format(id=self.id, dt=self.creation_time, load_avg_1min=self.load_avg_1min)

	def set_init_time(self):
		""" We'll store the current datetime used to represent the instance of the `uptime` results.
		We strip off the microseconds so that we can do an easier scan/comparison.

		returns a Datetime Object
		"""
		dt = datetime.datetime.now()
		dt = dt.replace(microsecond=0)
		return dt

	def set_load_averages(self):
		""" Initalize all the load averages for posterity.

		The `uptime` command returns a string representation in this structure:
		"{current_time} {system_uptime} {num_of_users} {system_load_avg_1min} {system_load_avg_5min} {system_load_avg_15min}"

		The easiest way to pull the load averages is just take the last three values.
		"""
		split_output = self.raw_uptime.split()
		filtered_output = split_output[len(split_output) - 3:len(split_output)]
		
		for duration, load_avg in zip([1, 5, 15], filtered_output):
			setattr(self, "load_avg_{}min".format(duration), float(load_avg))

	def check_load_avg(self, load_avg_duration_to_check, total_uptime_dict, num_of_cores):
		""" Check the load avg for the last two minutes to see if it exceeds 100%

		Since the os.system('uptime') command gives the load avg for the last minute. We'll take the most recent uptime
		and the uptime from exactly a minute ago, average those two out, and when dividing by the number of cores, see if it's > 1.

		load_avg_duration_to_check (int): Sets the duration we want (in minutes) to use for average for average load time.
										   i.e. average for the last two minutes
		total_uptime_dict (dictionary): The dictionary the process uses to store all the uptime statuses, keyed by its datetime. 
		num_of_cores: Number of cores in this particular machine. Used for the load calculation.

		returns avg_load_impact (float)
		"""
		one_min_ago_datetime = self.creation_time - datetime.timedelta(minutes=1)

		if one_min_ago_datetime not in total_uptime_dict:
			print "Can't find one_min_ago_datetime, needs to run for at least a minute before I can do comparison ", datetime.datetime.now()
			return
		
		# Get the load avg for the previous minute and calulate average load for the duration specified.
		prev_load_avg_1min = total_uptime_dict[one_min_ago_datetime].load_avg_1min
		avg_load = (self.load_avg_1min + prev_load_avg_1min) / 2.
		avg_load_impact = avg_load / num_of_cores

		return avg_load_impact

	def check_alert_load_threshold(self, alert, checked_load_avg):
		""" Check the load_avg and see if it merits triggering an alert

		alert (bool): Is there a high alert detected.
		checked_load_avg (float): What is the current load adverage

		returns the alert and alert message
		"""
		alert_msg = None
		if not alert and checked_load_avg > AVG_LOAD_THRESHOLD:
			alert = True
			alert_msg = "High load generated an alert - load = {value}, triggered at {time}".format(value=checked_load_avg, time=datetime.datetime.now())
			self.alert_triggered = True
		elif alert and checked_load_avg < AVG_LOAD_THRESHOLD:
			alert = False
			alert_msg = "Recovered from high load, now at {value}. Triggered at {time}.".format(value=checked_load_avg, time=datetime.datetime.now())
			self.alert_triggered = False

		return alert, alert_msg


import time
from uptime_status import UptimeStatus, LOAD_DURATION_TO_CHECK, CORE_COUNT


def write_to_db(message, alert_msg):
	""" Helper function to write any messages to a file """
	with open('uptime_data.txt', 'a') as storage:
			storage.write(message + '\n')
			if alert_msg:
				storage.write(alert_msg + '\n')

def run_uptime_interval(interval=10, loop_forever=True):
	""" Runs a process that checks load avg and alert logic and writes any messages to be retrieved from the frontend

	interval     (int): How long should we sleep before creating a new UptimeStatus instance and checking loads
	loop_forever (bool): Exits the function if we only want a single run through. 
	"""
	total_uptime_dict = {}
	alert = False
	instance_id = 1

	while True:
		alert_msg = None
		uptime_status_obj = UptimeStatus(id=instance_id)
		total_uptime_dict[uptime_status_obj.creation_time] = uptime_status_obj
		checked_load_avg = uptime_status_obj.check_load_avg(LOAD_DURATION_TO_CHECK, total_uptime_dict, CORE_COUNT) 
		alert, alert_msg = uptime_status_obj.check_alert_load_threshold(alert, checked_load_avg)
		instance_id += 1

		message = "{} ------ Current {} min load avg is: {}".format(uptime_status_obj.__str__(), LOAD_DURATION_TO_CHECK, checked_load_avg)
		write_to_db(message, alert_msg)

		if not loop_forever:
			return

		time.sleep(interval)

if __name__ == '__main__':
	run_uptime_interval()



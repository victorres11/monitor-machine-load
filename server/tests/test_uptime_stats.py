import unittest
from datetime import datetime
from mock import Mock, patch

from server.uptime_status import UptimeStatus, AVG_LOAD_THRESHOLD, LOAD_DURATION_TO_CHECK


class TestAlertLogic(unittest.TestCase):
	def setUp(self):
		self.num_of_cores = 4
		self.load_duration_to_check = LOAD_DURATION_TO_CHECK
		self.uptime_total_dict = {}

	def given_normal_load_avg(self, instance_id=1):
		uptime_obj = UptimeStatus(id=instance_id)
		uptime_obj.alert_triggered = False
		return uptime_obj

	@patch.object(UptimeStatus, 'check_load_avg', return_value=AVG_LOAD_THRESHOLD * 2, autospec=True)
	def when_load_check_exceeds_threshold(self, uptime_obj, mock):
		checked_load_avg = uptime_obj.check_load_avg(self.load_duration_to_check, self.uptime_total_dict, self.num_of_cores)
		return checked_load_avg

	def when_alert_threshold_checked(self, uptime_obj, checked_load_avg, current_alert_status=False):
		alert, alert_msg = uptime_obj.check_alert_load_threshold(current_alert_status, checked_load_avg)
		return alert, alert_msg, uptime_obj

	@patch.object(UptimeStatus, 'check_load_avg', return_value=AVG_LOAD_THRESHOLD / 2, autospec=True)
	def when_load_check_below_threshold(self, uptime_obj, mock):
		checked_load_avg = uptime_obj.check_load_avg(self.load_duration_to_check, self.uptime_total_dict, self.num_of_cores)
		return checked_load_avg

	def then_high_load_alert_is_triggered(self, uptime_obj, alert, alert_msg):
		self.assertTrue(alert)
		self.assertTrue(uptime_obj.alert_triggered)
		self.assertIn('High load generated an alert', alert_msg)

	def then_no_alert_is_triggered(self, uptime_obj, alert, alert_msg):
		self.assertFalse(alert)
		self.assertFalse(uptime_obj.alert_triggered)
		self.assertIsNone(alert_msg)

	def then_recovered_load_alert_is_triggered(self, uptime_obj, alert, alert_msg):
		self.assertFalse(alert)
		self.assertFalse(uptime_obj.alert_triggered)
		self.assertIn('Recovered from high load', alert_msg)


	def test_high_load_alert_triggered(self):
		uptime_obj = self.given_normal_load_avg(instance_id=1)
		high_load_avg = self.when_load_check_exceeds_threshold(uptime_obj)
		alert, alert_msg, uptime_obj = self.when_alert_threshold_checked(uptime_obj, high_load_avg, current_alert_status=False)
		self.then_high_load_alert_is_triggered(uptime_obj, alert, alert_msg)

	def test_no_alert_triggerd(self):
		uptime_obj = self.given_normal_load_avg(instance_id=2)
		low_load_avg = self.when_load_check_below_threshold(uptime_obj)
		alert, alert_msg, uptime_obj = self.when_alert_threshold_checked(uptime_obj, low_load_avg, current_alert_status=False)
		self.then_no_alert_is_triggered(uptime_obj, alert, alert_msg)

	def test_recovered_load_alert_triggered(self):
		uptime_obj = self.given_normal_load_avg(instance_id=3)
		high_load_avg = self.when_load_check_exceeds_threshold(uptime_obj)
		alert, alert_msg, uptime_obj = self.when_alert_threshold_checked(uptime_obj, high_load_avg, current_alert_status=False)

		low_load_avg = self.when_load_check_below_threshold(uptime_obj)
		alert, alert_msg, uptime_obj = self.when_alert_threshold_checked(uptime_obj, low_load_avg, current_alert_status=True)		
		self.then_recovered_load_alert_is_triggered(uptime_obj, alert, alert_msg)



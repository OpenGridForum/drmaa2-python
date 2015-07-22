import unittest
import drmaa2

class GeneralTestCase(unittest.TestCase):
	def test_struct_empty_init(self):
		""" Make sure that the data structures are properly initialized. """
		queue_info = drmaa2.QueueInfo()
		self.assertEqual(queue_info.name, None)

	def test_struct_param_init(self):
		""" Test data structure initialization on creation. """
		jt = drmaa2.JobTemplate(**{'remote_command':'/bin/sleep', 'submit_as_hold':True})
		self.assertEqual(jt.remote_command, '/bin/sleep')
		self.assertEqual(jt.submit_as_hold, True)

	def test_struct_backend_specific_attrs(self):
		""" Test that implementation-specific attributes are supported. """
		jt = drmaa2.JobTemplate()
		self.assertEqual(jt.mock_testattr, None)

class SessionManagerTestCase(unittest.TestCase):
	def test_describe_attribute(self):
		drmaa2.describe_attribute(drmaa2.Notification(), "sessionName")

	def test_supports(self):
		self.assertEqual(drmaa2.supports(drmaa2.Capability.CALLBACK), True)
		self.assertEqual(drmaa2.supports(drmaa2.Capability.ADVANCE_RESERVATION), True)

	def test_job_session(self):
		session = drmaa2.create_job_session()
		name = session.session_name
		session.close()
		session = drmaa2.open_job_session(name)
		session.close()
		drmaa2.destroy_session(name)

	def test_reservation_session(self):
		session = drmaa2.create_reservation_session()
		name = session.session_name
		session.close()
		session = drmaa2.open_reservation_session(name)
		session.close()
		drmaa2.destroy_session(name)

	def test_monitoring_session(self):
		session = drmaa2.open_monitoring_session()
		session.close()

	def test_get_job_session_names(self):
		drmaa2.get_job_session_names()

	def test_get_reservation_session_names(self):
		drmaa2.get_reservation_session_names()

	def _callback(notification):
		pass

	def test_register_event_notification(self):
		drmaa2.register_event_notification(self._callback)

class MonitoringSessionTestCase(unittest.TestCase):
	def test_get_all_jobs(self):
		session = drmaa2.open_monitoring_session("Foo")
		session.get_all_jobs("foo")

class JobSessionTestCase(unittest.TestCase):
	def test_run_job_with_contact(self):
		session = drmaa2.create_job_session("sessioName", "contact")
		jt = drmaa2.JobTemplate({'remoteCommand':'/bin/sleep'})
		job = session.run_job(jt)
		job.wait_terminated(drmaa2.INFINITE_TIME)

	def test_run_job_without_contact(self):
		session = drmaa2.create_job_session()
		jt = drmaa2.JobTemplate({'remoteCommand':'/bin/sleep'})
		job = session.run_job(jt)
		job.wait_terminated(drmaa2.INFINITE_TIME)

if __name__ == '__main__':
    unittest.main()
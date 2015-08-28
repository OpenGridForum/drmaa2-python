""" DRMAA2 Python language binding.

    This is a mock implementation for testing purposes.

    For further information, please visit drmaa.org.
"""

import drmaa2

# Definition part

job_template_impl_spec = ['mock_testattr']
job_info_impl_spec = []
reservation_template_impl_spec = []
reservation_info_impl_spec = []
queue_info_impl_spec = []
machine_info_impl_spec = []
notification_impl_spec = []

CORE_FILE_SIZE = "CORE_FILE_SIZE"
CPU_TIME = "CPU_TIME"
DATA_SIZE = "DATA_SIZE"
FILE_SIZE = "FILE_SIZE"
OPEN_FILES = "OPEN_FILES"
STACK_SIZE = "STACK_SIZE"
VIRTUAL_MEMORY = "VIRTUAL_MEMORY"
WALLCLOCK_TIME = "WALLCLOCK_TIME"

drms_name = "Mock DRM"
drms_version = {'major': 1, 'minor': 0}
drmaa_name = "Mock DRM DRMAA Implementation"
drmaa_version = {'major': 2, 'minor': 0}

# Implementation part

app_callback = None


def describe_attribute(instance, name):
    return name


class MonitoringSession(drmaa2.MonitoringSession):
    def get_all_reservations(self):
        return []

    def get_all_jobs(self, filter):
        return []

    def get_all_queues(self, names):
        return []

    def get_all_machines(self, names):
        return []

    def close(self):
        pass


class JobSession:
    contact = None
    session_name = None
    job_categories = None

    def get_jobs(self, filter):
        return []

    def get_job_array(self, job_array_id):
        return JobArray()

    def run_job(self, job_template):
        return Job()

    def run_bulk_jobs(self, job_template, begin_index, end_index, step, max_parallel):
        return JobArray()

    def wait_any_started(self, jobs, timeout):
        return Job()

    def wait_any_terminated(self, jobs, timeout):
        return Job()

    def close(self):
        pass


class ReservationSession:
    contact = None
    session_name = None

    def get_reservation(self, reservation_id):
        return Reservation()

    def request_reservation(self, reservation_template):
        return Reservation()

    def get_reservations(self):
        return []

    def close(self):
        pass


class Job:
    job_id = None
    session_name = None
    job_template = None

    def suspend(self):
        pass

    def resume(self):
        pass

    def hold(self):
        pass

    def release(self):
        pass

    def terminate(self):
        pass

    def reap(self):
        pass

    def get_state(self):
        return JobState.RUNNING, "Running like hell."

    def get_info(self):
        return JobInfo()

    def wait_started(self, timeout):
        pass

    def wait_terminated(self, timeout):
        pass

# Module-level functions


def describe_attribute(instance, name):
    return name


def supports(capability):
    if capability in (drmaa2.Capability.CALLBACK, drmaa2.Capability.ADVANCE_RESERVATION):
        return True
    else:
        return False


def create_job_session(session_name=None, contact=None):
    return JobSession()


def create_reservation_session(session_name=None, contact=None):
    return ReservationSession()


def open_job_session(session_name):
    return JobSession()


def open_reservation_session(session_name):
    return ReservationSession()


def open_monitoring_session(contact=None):
    return MonitoringSession()


def destroy_session(session):
    pass


def get_job_session_names():
    return []


def get_reservation_session_names():
    return []


def register_event_notification(callback):
    app_callback = callback

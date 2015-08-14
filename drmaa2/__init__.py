""" DRMAA2 Python language binding.

    This is the public interface to be used by applications.

    For further information, please visit drmaa.org.
"""

from enum import Enum
from collections import namedtuple
from abc import ABCMeta, abstractmethod

# Implementation-independent constants

HOME_DIR = "$DRMAA2_HOME_DIR$"
WORKING_DIR = "$DRMAA2_WORKING_DIR$"
PARAMETRIC_INDEX = "$DRMAA2_INDEX$"
INFINITE_TIME = -1
ZERO_TIME = 0

# Implementation-independent enumerations


class JobState(Enum):
    UNDETERMINED = 0
    QUEUED = 1
    QUEUED_HELD = 2
    RUNNING = 3
    SUSPENDED = 4
    REQUEUED = 5
    REQUEUED_HELD = 6
    DONE = 7
    FAILED = 8


class OperatingSystem(Enum):
    OTHER_OS = 0
    AIX = 1
    BSD = 2
    LINUX = 3
    HPUX = 4
    IRIX = 5
    MACOS = 6
    SUNOS = 7
    TRU64 = 8
    UNIXWARE = 9
    WIN = 10
    WINNT = 11


class CpuArchitecture(Enum):
    OTHER_CPU = 0
    ALPHA = 1
    ARM = 2
    ARM64 = 3
    CELL = 4
    PARISC = 5
    PARISC64 = 6
    X86 = 7
    X64 = 8
    IA64 = 9
    MIPS = 10
    MIPS64 = 11
    PPC = 12
    PPC64 = 13
    PPC64LE = 16
    SPARC = 14
    SPARC64 = 15


class Event(Enum):
    NEW_STATE = 0
    MIGRATED = 1
    ATTRIBUTE_CHANGE = 2


class Capability(Enum):
    ADVANCE_RESERVATION = 0
    RESERVE_SLOTS = 1
    CALLBACK = 2
    BULK_JOBS_MAXPARALLEL = 3
    JT_EMAIL = 4
    JT_STAGING = 5
    JT_DEADLINE = 6
    JT_MAXSLOTS = 7
    JT_ACCOUNTINGID = 8
    RT_STARTNOW = 9
    RT_DURATION = 10
    RT_MACHINEOS = 11
    RT_MACHINEARCH = 12

# Abstract classes, to be realized by implementation


class ReservationSession:
    """ Every ReservationSession instance acts as container for advance reservations in the DRM system. """
    __metaclass__ = ABCMeta

    contact = None
    session_name = None

    @abstractmethod
    def get_reservation(self, reservation_id):
        """ get_reservation(self, str) -> Reservation

            This method returns the Reservation instance that has the given reservationId.
        """
        pass

    @abstractmethod
    def request_reservation(self, reservation_template):
        """ request_reservation(self, ReservationTemplate) -> Reservation

        The method requests an advance reservation in the DRM system as described
        by the ReservationTemplate instance. On success,
        the method returns an object that represents the advance reservation
        in the underlying DRM system.
        """
        pass

    @abstractmethod
    def get_reservations(self):
        """ get_reservations(self) -> list

            This method returns a list of Reservation objects for the reservations in this session,
            regardless of their start and end time.
        """
        pass

    @abstractmethod
    def close(self):
        """ close(self) -> None

            The method performs the necessary actions to disengage from the DRM system.
        """
        pass


class Reservation:
    """ The Reservation class represents attributes and methods available for an
        advance reservation successfully created in the DRM system.
    """
    __metaclass__ = ABCMeta

    reservation_id = None
    session_name = None
    reservation_template = None

    @abstractmethod
    def get_info(self):
        """ get_info(self) -> ReservationInfo

            This method returns informations about this advanced reservation.
        """
        pass

    @abstractmethod
    def terminate(self):
        """ terminate(self) -> None

            This method terminates the advance reservation represented by this instance.
        """
        pass


class JobArray:
    """ An instance of the JobArray interface represents a set of jobs created by one operation.

        The job control functions allow modifying the status of the job array in the DRM system,
        with the same semantic as in the Job object.
    """
    __metaclass__ = ABCMeta

    job_array_id = None
    jobs = None
    session_name = None
    job_template = None

    @abstractmethod
    def suspend(self):
        """ suspend(self) -> None """
        pass

    @abstractmethod
    def resume(self):
        """ resume(self) -> None """
        pass

    @abstractmethod
    def hold(self):
        """ hold(self) -> None """
        pass

    @abstractmethod
    def release(self):
        """ release(self) -> None """
        pass

    @abstractmethod
    def terminate(self):
        """ terminate(self) -> None """
        pass

    @abstractmethod
    def reap(self):
        """ reap(self) -> None

        This function performs a Job.reap() operation for each of the jobs in the array.
        """
        pass


class JobSession:
    """ A job session acts as container for job instances controlled through the DRMAA API.
       The session methods support the submission of new jobs and the monitoring of existing jobs.
       The relationship between jobs and their session is persisted.
    """
    __metaclass__ = ABCMeta

    contact = None
    session_name = None
    job_categories = None

    @abstractmethod
    def get_jobs(self, filter=None):
        """ get_jobs(self, JobInfo) -> list

            This method returns a list of job objects that belong to the job session.

            The filter parameter allows to choose a subset of the session jobs as return value.
            If filter is None, all session jobs are returned.
        """
        pass

    @abstractmethod
    def get_job_array(self, job_array_id):
        """ get_job_array(self, str) -> JobArray

            This method returns the JobArray instance with the given ID.
        """
        pass

    @abstractmethod
    def run_job(self, job_template):
        """ run_job(self, JobTemplate) -> Job

            The run_job method submits a job with the attributes defined in the given job template instance.
            The method returns a Job object that represents the job in the underlying DRM system.
        """
        pass

    @abstractmethod
    def run_bulk_jobs(self, job_template, begin_index, end_index, step, max_parallel=None):
        """ run_bulk_jobs(self, JobTemplate, long, long, long, long) -> JobArray

            The runBulkJobs method creates a set of parametric jobs, each with attributes as defined
            in the given job template instance. Each job in the set has the same attributes,
            except for the job template attributes that include the PARAMETRIC_INDEX macro.

            The method returns a JobArray instance that represents the set of Job objects created
            by the method call under a common array identity.

            The first job in the set has an index equal to the beginIndex parameter of the method call.
            The smallest valid value for beginIndex is 1.
            The next job has an index equal to beginIndex + step, and so on.
            The last job has an index equal to beginIndex + n * step, where n is equal
            to (endIndex - beginIndex) / step.
            The index of the last job may not be equal to endIndex if the difference between beginIndex and
            endIndex is not evenly divisible by step. The beginIndex value must be less than or equal to endIndex,
            and only positive index numbers are allowed

            The maxParallel parameter allows to specify how many of the bulk job instances are allowed to run
            in parallel on the utilized resources. If the parameter is None, no limit is applied.
        """
        pass

    @abstractmethod
    def wait_any_started(self, jobs, timeout):
        """ wait_any_started(self, list, long) ->  Job

            The method blocks until any of the jobs in the list entered one of the 'Started' states.

            The timeout argument specifies the desired maximum waiting time for the state change in seconds.
            The constant value INFINITE_TIME declares an indefinite waiting time.
            The constant value ZERO_TIME declares that the method call must return immediately.
        """
        pass

    @abstractmethod
    def wait_any_terminated(self, jobs, timeout):
        """ wait_any_terminated(self, list, time_amount) -> Job

            The method blocks until any of the jobs in the list entered one of the 'Terminated' states.

            The timeout argument specifies the desired maximum waiting time for the state change in seconds.
            The constant value INFINITE_TIME declares an indefinite waiting time.
            The constant value ZERO_TIME declares that the method call must return immediately.
        """
        pass

    @abstractmethod
    def close(self):
        """ close(self) -> None

            The method performs the necessary actions to disengage from the DRM system.
        """
        pass


class Job:
    """ Every job in the JobSession is represented by its own instance of the Job class.
        It allows to instruct the DRM system of a job status change, and to query the properties
        of the job in the DRM system.
    """
    __metaclass__ = ABCMeta

    job_id = None
    session_name = None
    job_template = None

    @abstractmethod
    def suspend(self):
        """ suspend(self) -> None """
        pass

    @abstractmethod
    def resume(self):
        """ resume(self) -> None """
        pass

    @abstractmethod
    def hold(self):
        """ hold(self) -> None """
        pass

    @abstractmethod
    def release(self):
        """ release(self) -> None """
        pass

    @abstractmethod
    def terminate(self):
        """ terminate(self) -> None """
        pass

    @abstractmethod
    def reap(self):
        """ reap(self) -> None

        This function is intended to let the DRMAA implementation clean up any data about this job.
        The motivating factor are long-running applications maintaining large amounts of jobs as part of
        a monitoring session.
        Using a reaped job in any subsequent activity generates an InvalidArgumentException.
        This function only works for terminated jobs.
        """
        pass

    @abstractmethod
    def get_state(self):
        """ get_state(self) -> JobState, str

            This method allows the application to get the current status of the job.
            It returns the status according to the DRMAA state model as JobState enumeration value.
            In addition, an implementation-specific sub state is returned as string.
        """
        pass

    @abstractmethod
    def get_info(self):
        """ get_info(self) -> JobInfo

            This method returns a JobInfo instance for the job.
        """
        pass

    @abstractmethod
    def wait_started(self, timeout):
        """ wait_started(self, long) -> None

            The method blocks until the job entered one of the 'Started' states.

            The timeout argument specifies the desired maximum waiting time for the state change in seconds.
            The constant value INFINITE_TIME declares an indefinite waiting time.
            The constant value ZERO_TIME declares that the method call must return immediately.
        """
        pass

    @abstractmethod
    def wait_terminated(self, timeout):
        """ wait_terminated(self, long) -> None

            The method blocks until the job entered one of the 'Terminated' states.

            The timeout argument specifies the desired maximum waiting time for the state change in seconds.
            The constant value INFINITE_TIME declares an indefinite waiting time.
            The constant value ZERO_TIME declares that the method call must return immediately.
        """
        pass


class MonitoringSession:
    """ The MonitoringSession class provides a set of stateless methods for fetching information
        about the DRM system and the DRMAA implementation itself.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_reservations(self):
        """ get_all_reservations(self) -> list

            This method returns a list of Reservation objects, which represent all advance reservations visible
            for the user running the DRMAA-based application.

            In contrast to a ReservationSession.get_reservations() call,
            this method may also return reservations that were created outside of DRMAA,
            e.g., through command-line tools by this user.

            The DRM system or the DRMAA implementation is at liberty to restrict the set of returned
            reservations based on site or system policies, such as security settings or
            scheduler load restrictions. The returned list may contain reservations that were created
            by other users. It may also contain reservations that are not usable for the user.
        """
        pass

    @abstractmethod
    def get_all_jobs(self, filter=None):
        """ get_all_jobs(self, JobInfo) -> list

            This method returns a list of Job objects, representing all DRMS jobs visible to the user running
            the DRMAA-based application.

            The filter argument, if given, allows to fetch only a subset of the available job information.

            In contrast to a JobSession.get_jobs() call, this method may also return
            jobs that were submitted outside of DRMAA (e.g., through command-line tools) by this user.
            The returned list may also contain jobs that were submitted by other users if the security policies
            of the DRM system allow such global visibility. The DRM system or the DRMAA implementation is at liberty,
            however, to restrict the set of returned jobs based on site or system policies, such as security settings
            or scheduler load restrictions.
        """
        pass

    @abstractmethod
    def get_all_queues(self, names=None):
        """ get_all_queues(self, list) -> list

            This method returns a list of QueueInfo objects, representing the queues available for job submission in the
            DRM system. The names from all instances in this list can be used in the JobTemplate.queueName attribute.

            The names parameter is a list of strings. If given, then it will restrict the result to QueueInfo instances
            that have one of the names given in the list.

            The result can be an empty list or might be incomplete, based on queue, host, or system policies.
            It might also contain queues that are not accessible for the user at job submission time because of
            queue configuration limits.
        """
        pass

    @abstractmethod
    def get_all_machines(self, names):
        """ get_all_machines(self, list) -> list

            This method returns a list of MachineInfo objects, each representing a machine available in the DRM system
            as execution host.

            The names parameter is a list of strings. If given, then it will restrict the result to MachineInfo
            instances that have one of the names given in the list.

            The returned list might be empty or incomplete based on machine or system policies. It might also contain
            machines that are not accessible for the user, e.g., because of host configuration limits.
        """
        pass

    @abstractmethod
    def close(self):
        """ close(self) -> None

            The method performs the necessary actions to disengage from the DRM system.
        """
        pass

# Import implementation

from drmaa2.backend import impl

# Implementation-dependent constants

CORE_FILE_SIZE = impl.CORE_FILE_SIZE
CPU_TIME = impl.CPU_TIME
DATA_SIZE = impl.DATA_SIZE
FILE_SIZE = impl.FILE_SIZE
OPEN_FILES = impl.OPEN_FILES
STACK_SIZE = impl.STACK_SIZE
VIRTUAL_MEMORY = impl.VIRTUAL_MEMORY
WALLCLOCK_TIME = impl.WALLCLOCK_TIME

# Implementation-dependent constants determined at module loading

drms_name = impl.drms_name
drms_version = impl.drms_version
drmaa_name = impl.drmaa_name
drmaa_version = impl.drmaa_version
job_template_impl_spec = impl.job_template_impl_spec
job_info_impl_spec = impl.job_info_impl_spec
reservation_template_impl_spec = impl.reservation_template_impl_spec
reservation_info_impl_spec = impl.reservation_info_impl_spec
queue_info_impl_spec = impl.queue_info_impl_spec
machine_info_impl_spec = impl.machine_info_impl_spec
notification_impl_spec = impl.notification_impl_spec

# Extensible data structures

# TODO: Distinguish mandatory and optional ones, fetch optional from implementation

Notification = namedtuple('Notification', ['event', 'job_id', 'session_name', 'job_state']
                          + impl.notification_impl_spec)
Notification.__new__.__defaults__ = tuple([None]*len(Notification._fields))

JobTemplate = namedtuple('JobTemplate', ['remote_command', 'args', 'submit_as_hold', 'rerunnable',
                                         'job_environment', 'working_directory', 'job_category',
                                         'email', 'email_on_started', 'email_on_terminated', 'job_name',
                                         'input_path', 'output_path', 'error_path', 'join_files',
                                         'reservation_id', 'queue_name', 'min_slots', 'max_slots',
                                         'priority', 'candidate_machines', 'min_phys_memory', 'machine_os',
                                         'machine_arch', 'start_time', 'deadline_time', 'stage_in_files',
                                         'stage_out_files', 'resource_limits', 'accounting_id']
                         + impl.job_template_impl_spec)
JobTemplate.__new__.__defaults__ = tuple([None]*len(JobTemplate._fields))

QueueInfo = namedtuple('QueueInfo', ['name'] + impl.queue_info_impl_spec)
QueueInfo.__new__.__defaults__ = tuple([None]*len(QueueInfo._fields))

JobInfo = namedtuple('JobInfo', ['job_id', 'job_name', 'exit_status', 'terminating_signal', 'annotation', 'job_state',
                                 'job_sub_state', 'allocated_machines', 'submission_machine', 'job_owner', 'slots',
                                 'queue_name', 'wallclock_time', 'cpu_time', 'submission_time', 'dispatch_time',
                                 'finish_time'] + impl.job_info_impl_spec)
JobInfo.__new__.__defaults__ = tuple([None]*len(JobInfo._fields))

MachineInfo = namedtuple('MachineInfo', ['name', 'available', 'sockets', 'cores_per_socket', 'threads_per_core',
                                         'load', 'phys_memory', 'virt_memory', 'machine_os', 'machine_os_version',
                                         'machine_arch'] + impl.machine_info_impl_spec)
MachineInfo.__new__.__defaults__ = tuple([None]*len(MachineInfo._fields))

ReservationInfo = namedtuple('ReservationInfo', ['reservation_id', 'reservation_name', 'reserved_start_time',
                                                 'reserved_end_time', 'users_acl', 'reserved_slots',
                                                 'reserved_machines'] + impl.reservation_info_impl_spec)
ReservationInfo.__new__.__defaults__ = tuple([None]*len(ReservationInfo._fields))

ReservationTemplate = namedtuple('ReservationTemplate', ['reservation_name', 'start_time', 'end_time', 'duration',
                                                         'min_slots', 'max_slots', 'job_category', 'users_acl',
                                                         'candidate_machines', 'min_phys_memory', 'machine_os',
                                                         'machine_arch'] + impl.reservation_template_impl_spec)
ReservationTemplate.__new__.__defaults__ = tuple([None]*len(ReservationTemplate._fields))

SlotInfo = namedtuple('SlotInfo', ['machine_name', 'slots'])
SlotInfo.__new__.__defaults__ = (None, None)

Version = namedtuple('Version', ['major', 'minor'])
Version.__new__.__defaults__ = (None, None)


class DeniedByDrmsException(Exception):
    """ The DRM system rejected the operation due to security issues. """
    pass


class DrmCommunicationException(Exception):
    """ The DRMAA implementation could not contact the DRM system.
        The problem source is unknown to the implementation,
        so it is unknown if the problem is transient or not.
    """
    pass


class TryLaterException(Exception):
    """ The DRMAA implementation detected a transient problem while
        performing the operation, for example due to excessive load.
        The application is recommended to retry the operation.
    """
    pass


class TimeoutException(Exception):
    """ The timeout given in one the waiting functions was reached
        without successfully finishing the waiting attempt.
    """
    pass


class InternalException(Exception):
    """ An unexpected or internal error occurred in the DRMAA library,
        for example a system call failure.
        It is unknown if the problem is transient or not.
    """
    pass


class InvalidArgumentException(Exception):
    """ From the viewpoint of the DRMAA library, an input parameter for
        the particular method call is invalid or inappropriate.
    """
    pass


class InvalidSessionException(Exception):
    """ The session used for the method call is not valid,
        for example since the session was previously closed.
    """
    pass


class InvalidStateException(Exception):
    """ The operation is not allowed in the current state of the job. """
    pass


class OutOfResourceException(Exception):
    """ The implementation has run out of operating system resources,
        such as buffers, main memory, or disk space.
    """
    pass


class UnsupportedAttributeException(Exception):
    """ The optional attribute is not supported by this DRMAA implementation. """
    pass


class UnsupportedOperationException(Exception):
    """ The method is not supported by this DRMAA implementation."""
    pass


class ImplementationSpecificException(Exception):
    """ The implementation needs to report a special error condition that
        cannot be mapped to one of the other exceptions.
    """
    pass


# Module-level functions

def supports(capability):
    """ supports(Capability entry) -> bool

        This method allows to test if the DRMAA implementation supports a feature specified as optional.
        The allowed input values are specified in the Capability enumeration.
    """
    return impl.supports(capability)


def create_job_session(session_name=None, contact=None):
    """ create_job_session(str, str) -> JobSession object

        The method creates and opens a new job session.
    """
    return impl.create_job_session(session_name, contact)


def create_reservation_session(session_name=None, contact=None):
    """ create_reservation_session(str, str) -> ReservationSession object

        The method creates and opens a new reservation session.
    """
    return impl.create_reservation_session(session_name, contact)


def open_job_session(session_name):
    """ open_job_session(str) -> JobSession object

        The method opens an existing job session.
    """
    return impl.open_job_session(session_name)


def open_reservation_session(session_name):
    """ open_reservation_session(str) -> ReservationSession object

        The method opens an existing reservation session.
    """
    return impl.open_reservation_session(session_name)


def open_monitoring_session(contact=None):
    """ open_monitoring_session(str) -> MonitoringSession object

        The method opens a monitoring session.
    """
    return impl.open_monitoring_session(contact)


def destroy_session(session):
    """ destroy_session(str) -> None

        The method reaps all persistent or cached state information for the given session name.
    """
    impl.destroy_session(session)


def get_job_session_names():
    """ get_job_session_names() -> list

        This method returns a string list of job session names that are valid input for the open_job_session method.
    """
    return impl.get_job_session_names()


def get_reservation_session_names():
    """ get_reservation_session_names() -> list

        This method returns a string list of reservation session names that are valid input for
        the open_reservation_session method.
    """
    return impl.get_reservation_session_names()


def register_event_notification(callback):
    """ register_event_notification(function) -> None

    This method is used to register a callback function for events from the DRM system.
    The function should accept one parameter that is filled with a Notification object.
    """
    impl.register_event_notification(callback)


def describe_attribute(instance, name):
    """ describe_attribute(namedtuple, str) -> str

        Returns a human-readable description of an attributes purpose in the instance.
    """
    return impl.describe_attribute(instance, name)

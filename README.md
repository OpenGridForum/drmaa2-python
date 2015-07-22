# DRMAA2 Python language binding

This repository offers a reference implementation for the DRMAA2 Python language binding.   

If you don't know what DRMAA is, please consult http://www.drmaa.org.

The code base is maintained by members of the Open Grid Forum (OGF) DRMAA group. The intention is to have a common starting point for true product implementations of the DRMAAv2 Python language binding. We keep the interface definitions in this code synchronized to our OGF DRMAA standards, so that you don't need the documents - at least at the beginning. 

The source code licence is 'Apache 2.0', which should allow you the unrestricted usage in both closed source and open source projects.

The drmaa2 module file is expected to be re-used without modification, typically in a forked project. If you see a need to change it, please talk to us, in order to maintain portability and standard compliance across all implementations of this language binding.

The mock.py code in the drmaa2.backend module supports only the test suite operation. Your drmaa2-python implementation is expected to add another file in this module with a true implementation. Your resulting Python package can then replace the on-liner in drmaa2/backend/__init__.py accordingly.

We would be happy if you give us a hint if this code was helpful for you. Additions to the test suite are also more than welcome.

## Compatibility

This code is designed to work with Python 2.6 and all later version, including Python 3. Implementers are encouraged to follow this convention.

The library dependencies for Python 2 environments are listed in requirements_py2.txt.

## Note to DRMAA users

If you are looking for a DRMAA2 Python library for your cluster system, this is the wrong place (at the moment). Check forks of this repository to figure out if your cluster environment already has a matching implementation. Talk to your DRM vendor and express your demand.

## Future plans

Future versions of this code will work on-top of the DRMAA2 C library interface. This would make this code directly usable with multiple DRM systems. A PyPi release will be done if such an implementation is given.

People may also implement this interface on-top of the DRMAA1 C library interface or with wrapped command-line calls (bad idea). 

## Example

	import drmaa2
	session = drmaa2.create_job_session()
	jt = drmaa2.JobTemplate({'remoteCommand':'/bin/sleep'})
	job = session.run_job(jt)
	job.wait_terminated(drmaa2.INFINITE_TIME)

---
The OGF DRMAA Working Group <drmaa-wg@ogf.org>

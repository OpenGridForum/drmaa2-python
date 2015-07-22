# DRMAA2 Python language binding

This repository offers a reference implementation for the DRMAA2 Python language binding.   

If you don't know what DRMAA is, please consult http://www.drmaa.org.

The code base is maintained by members of the Open Grid Forum (OGF) DRMAA group. The intention is to have a common starting point for true product implementations. We keep this code synchronized to our OGF DRMAA standards, so that you don't need to read the documents at the beginning. Later, you can consult [GFD-R-P.194](https://www.ogf.org/documents/GFD.194.pdf) for details.

The `drmaa2/__init__.py` file is expected to remain untouched. If you see a need to change it, please talk to us, in order to maintain portability and standard compliance across all implementations.

The mock.py code in the drmaa2.backend module supports the test suite only. Vendors are expected to add another file with a true implementation and replace the on-liner in `drmaa2/backend/__init__.py` accordingly.

We would be happy if you give us a hint if this code was helpful for you. Additions to the test suite are also more than welcome.

## Compatibility

This code is designed to work with Python 2.6 and all later version, including Python 3. Implementers are encouraged to follow this convention.

The library dependencies for Python 2 environments are listed in requirements_py2.txt.

## Note to DRMAA users

If you are looking for a DRMAA2 Python library for your cluster system, this is the wrong place (at the moment). Check forks of this repository for true implementations, and talk to your DRM vendor.

## Future plans

Future versions of this code will work on-top of the DRMAA2 C library interface. This would make it directly usable with multiple DRM systems. A PyPi release will be done if such an implementation is given.

People may also implement this interface on-top of the DRMAA1 C library interface or with wrapped command-line calls (bad idea). 

## Example

	import drmaa2
	session = drmaa2.create_job_session()
	jt = drmaa2.JobTemplate({'remoteCommand':'/bin/sleep'})
	job = session.run_job(jt)
	job.wait_terminated(drmaa2.INFINITE_TIME)

---
The OGF DRMAA Working Group <drmaa-wg@ogf.org>

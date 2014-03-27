pyand: Python library for adb and fastboot
=========================================

pyand is a simple Python library that allows you to easily work with adb and fastboot connected Android devices. 

Existing Python modules for adb are somewhat outdated or broken, hence why I went ahead and wrote pyand. I also wanted more than just adb hence why I added in support for Fastboot as well. Usage is simple and should be pretty intuitive for anyone used to working with adb and fastboot.

.. code-block:: pycon

    >>> adb = ADB()
    >>> adb.get_devices()
    {0: 'emulator-5554', 1: 'emulator-5556'}
    >>> adb.set_target_by_id(1)
    >>> adb.get_target_device()
    'emulator-5554'
    >>> adb.set_system_rw()
    'remount succeeded'
    ...

pyand will eventually let you do pretty much anything you could possibly do with adb and fastboot, but its still under development and not entirely done yet. 


Credits
========

pyand spawned from `pyadb <https://github.com/sch3m4/pyadb>`_ so thanks to Chema Garcia for writing it as it gave me a great starting point for pyand.


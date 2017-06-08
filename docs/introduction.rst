.. _introduction:

Getting Started
===============

Simple Example
--------------

pyand exposes two classes. ADB and Fastboot. Usage is simple and to verify that everything is set up correctly we can import ADB and Fastboot and check for connected devices::

     >>> from pyand import ADB, Fastboot
     >>> adb = ADB()
     >>> adb.get_devices()
     {0: '15901aabbccdd124', 1: 'abc1951124de1241'}
     >>> adb.set_target_by_id(1)
     '[+] Target device set: abc1951124de1241'
     >>> adb.get_model()
     'Nexus_5'
     >>> adb.set_system_rw()
     'remount succeeded'
     >>> adb.reboot(2)
     >>> fb = Fastboot()
     >>> fb.get_devices()
     {0: 'abc1951124de1241'}

To start we have to import the ADB and Fastboot classes to be able to access the associated methods. As long as the ADB and Fastboot binaries are in your $PATH the above example should work. Otherwise you will have to specify the path to binary when instantiating the object.::

    >>> adb = ADB('~/android-sdk/platform-tools/adb')

Furthermore, notice how we set a device target. Since you can have several devices connected it's important for pyand to know which device you want to interact with. 

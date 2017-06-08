.. _introduction:

Basics
===============
This section covers the most basic concepts in pyand

Devices
--------------
You can easily use adb to get a list of the currently connected devices.::
    
    >> from pyand import ADB
    >> adb = ADB()
    >> adb.get_devices()
    {0: '12601aabbccdd124', 1: 'abc1551124de1241'}

Notice how ``get_devices()`` returns a dictionary with an index and the device identifer.

Setting a target device
-----------------------
In order to interact with a device you need to tell pyand which device you want to interact with. You do this by specifying either the device index from the dictionary returned from ``get_devices()`` or by the device id.::
    
    >> adb.get_devices()
    {0: '12601aabbccdd124', 1: 'abc1551124de1241'}
    >> adb.set_target_by_id(1)
    [+] Target device set: abc1551124de1241
    >> adb.set_target_by_name('abc1551124de1241')
    [+] Target device set: abc1551124de1241


Getting device state
--------------------
Note how that dictionary returned by ``get_devices()`` does not indicate the state of the device(s). You can use ``get_state()`` for that. Remeber ot set a device target first.::

    >> adb.get_state()
    unauthorized



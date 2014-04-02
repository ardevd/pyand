pyand: Python library for adb and fastboot
=========================================

pyand is a simple Python library for Python 2.7 that allows you to easily work with adb and fastboot connected Android devices. 

Existing Python modules for adb are somewhat outdated or broken, hence why I went ahead and wrote pyand. I also wanted more than just adb hence why I added in support for Fastboot as well. Usage is simple and should be pretty intuitive for anyone used to working with adb and fastboot.

.. code-block:: pycon

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
    [+] fastboot executable found
    >>> fb.get_devices()
    {0: 'abc1951124de1241'}
    ...


pyand will eventually let you do pretty much anything you could possibly do with adb and fastboot, but its still under development and not entirely done yet. 

Requirements 
=======
* Python 2.7 is the recommended version of Python as Python 3.x is not currently supported.
* Fastboot and ADB is also required and should ideally be in your $PATH. If its not in your $PATH you will have to specify the path when you instantiate the object. 
  
    * `The Android SDK <https://developer.android.com/sdk/index.html>`_ is a good way of getting a hold of up-to-date binaries.

Documentation
====
The Wiki will eventually be a good place to find documentation. 

Installation
======
There are currently two recommended ways of installing pyand.


easy_install
-------
If you have easy_install for Python-2.7 installed, you can use it to install pyand pretty easily. 

.. code-block::

   $ git clone https://github.com/Zyg0te/pyand
   $ sudo easy_install-2.7 pyand


AUR PKGBUILD
----
There is also an officially supported PKGBUILD available. You can grab the PKGBUILD from the github repo or from the `AUR <https://aur.archlinux.org/packages/python2-pyand-git/>`_. You can install it like any other AUR package.

Credits
========

pyand spawned from `pyadb <https://github.com/sch3m4/pyadb>`_ so thanks to Chema Garcia for writing it as it gave me a great starting point for pyand.


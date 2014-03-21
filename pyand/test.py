from pyand import ADB
adb = ADB()
print adb.get_version()
print adb.check_path()
print adb.get_devices()

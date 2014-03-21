from pyand import ADB
adb = ADB("adb")
a = adb.get_version()
print a


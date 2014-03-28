try:
    import sys
    import subprocess
    from os import popen3 as pipe
except ImportError, e:
    # should never happen!
    print "[!] Required module missing. %s" % e.args[0]
    sys.exit(-1)

class Fastboot(object):

    __fastboot_path = None
    __output = None
    __error = None
    __devices = None
    __target = None

    def __init__(self, fastboot_path="fastboot"):
        """
        By default we assume fastboot is in $PATH
        """
        self.__fastboot_path = fastboot_path
        if not self.check_path():
            self.__error = "[!] fastboot path not valid."

    def __clean__(self):
        self.__output = None
        self.__error = None

    def __read_output__(self, fd):
        ret = ""
        while 1:
            line = fd.readline()
            if not line:
                break
            ret += line

        if len(ret) == 0:
            ret = None

        return ret

    def __build_command__(self, cmd):
            """
            Build command parameters for Fastboot command
            """
            if self.__devices is not None and len(self.__devices) > 1 and self.__target is None:
                self.__error = "[!] Must set target device first"
                return None

            if type(cmd) is tuple:
                a = list(cmd)
            elif type(cmd) is list:
                a = cmd
            else:
                a = cmd.split(" ")
            a.insert(0, self.__fastboot_path)
            if self.__target is not None:
                # add target device arguments to the command
                a.insert(1, '-s')
                a.insert(2, self.__target)

            return a

    def run_cmd(self, cmd):
        """
        Run a command against fastboot tool ($ fastboot <cmd>)
        """
        self.__clean__()

        if self.__fastboot_path is None:
            self.__error = "[!] Fastboot path not set"
            return False

        try:
            args = self.__build_command__(cmd)
            if args is None:
                return
            print 'args>', args
            cmdp = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.__output, self.__error = cmdp.communicate()
            retcode = cmdp.wait()
            return self.__output
        except OSError, e:
            self.__error = str(e)

        return

    def check_path(self):
        """
        Check if the Fastboot path is valid
        """
        if self.run_cmd("help") is None:
            print "[-] fastboot executable not found"
            return False
        print "[+] fastboot executable found"
        return True

    def set_fastboot_path(self, fastboot_path):
        """
        Set the Fastboot tool path
        """
        self.__fastboot_path = fastboot_path
        self.check_path()

    def get_fastboot_path(self):
        """
        Returns the Fastboot tool path
        """
        return self.__fastboot_path_path

    def get_devices(self):
        """
        Return a dictionary of fastboot connected devices along with an incremented Id.
        fastboot devices
        """
        error = 0
        #Clear existing list of devices
        self.__devices = None
        self.run_cmd("devices")
        if self.__error is not None:
            return ''
        try:
            device_list = self.__output.partition('\n')[2].replace('device','').split()

            if device_list[1:] == ['no','permissions']:
                error = 2
                self.__devices = None
        except:
            self.__devices = None
            error = 1
        #return (error,self.__devices)
        i = 0
        device_dict =  {}
        for device in device_list:
            #Add list to dictionary with incrementing ID
            device_dict[i] = device
            i += 1
        self.__devices = device_dict
        return self.__devices

    def set_target_by_name(self, device):
        """
        Specify the device name to target
        example: set_target_device('emulator-5554')
        """
        if device is None or not device in self.__devices.values():

            self.__error = 'Must get device list first'
            print "[!] Device not found in device list"
            return False
        self.__target = device
        return "[+] Target device set: %s" % self.get_target_device()

    def set_target_by_id(self, device):
        """
        Specify the device ID to target.
        The ID should be one from the device list.
        """
        if device is None or not device in self.__devices:
            self.__error = 'Must get device list first'
            print "[!] Device not found in device list"
            return False
        self.__target = self.__devices[0]
        return "[+] Target device set: %s" % self.get_target_device()

    def flash_all(self, wipe=False):
        """
        flash boot + recovery + system. Optionally wipe everything
        """
        if wipe:
            self.run_cmd('-w flashall')
        else:
            self.run_cmd('flashall')

    def reboot_device(self):
        """
        Reboot the device normally
        """
        self.run_cmd('reboot')
        return self.__output

    def reboot_device_bootloader(self):
        """
        Reboot the device into bootloader
        """
        self.run_cmd('reboot-bootloader')
        return self.__output
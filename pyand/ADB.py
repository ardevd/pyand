#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# Author: Edvard Holst
# Project Site: http://github.com/Zyg0te/pyand
# Version: 0.9.1.2
###

try:
    import sys
    import subprocess
    import re
    from os import popen3 as pipe
except ImportError as e:
    # should never be reached
    print "[!] Required module missing. %s" % e.args[0]
    sys.exit(-1)


class ADB(object):

    __adb_path = None
    __output = None
    __error = None
    __devices = None
    __target = None

    # reboot modes
    REBOOT_NORMAL = 0
    REBOOT_RECOVERY = 1
    REBOOT_BOOTLOADER = 2

    # default TCP/IP port
    DEFAULT_TCP_PORT = 5555
    # default TCP/IP host
    DEFAULT_TCP_HOST = "localhost"

    def __init__(self, adb_path="adb"):
        #By default we assume adb is in $PATH
        self.__adb_path = adb_path
        if not self.check_path():
            self.__error = "[!] adb path not valid"

    def __clean__(self):
        self.__output = None
        self.__error = None

    def __read_output__(self, fd):
        ret = ''
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
        Build command parameters
        """
        if self.__devices is not None and len(self.__devices) > 1 and self.__target is None:
            self.__error = "[!] Must set target device first"
            return None

        if type(cmd) is tuple:
            a = list(cmd)
        elif type(cmd) is list:
            a = cmd
        else:
            #All arguments must be single list items
            a = cmd.split(" ")

        a.insert(0, self.__adb_path)
        if self.__target is not None:
            # add target device arguments to the command
            a.insert(1, '-s')
            a.insert(2, self.__target)

        return a

    def run_cmd(self, cmd):
        """
        Run a command against adb tool ($ adb <cmd>)
        """
        self.__clean__()

        if self.__adb_path is None:
            self.__error = "[!] ADB path not set"
            return False

        try:
            args = self.__build_command__(cmd)
            if args is None:
                return
            #Print out args for debug purposes
            #print 'args>', args
            cmdp = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self.__output, self.__error = cmdp.communicate()
            retcode = cmdp.wait()
            return self.__output.rstrip('\n')
        except OSError, e:
            self.__error = str(e)

        return

    def get_version(self):
        """
        Returns ADB tool version
        adb version
        """
        ret = self.run_cmd("version")
        try:
            pattern = re.compile(r"version\s(.+)")
            version = pattern.findall(ret)[0]
        except:
            version = None
        return version

    def check_path(self):
        """
        Verify if adb path is valid
        """

        if self.get_version() is None:
            print "[-] adb executable not found"
            return False
        return True

    def set_adb_path(self,adb_path):
        """
        Set the ADB tool path
        """
        self.__adb_path = adb_path
        self.check_path()

    def get_adb_path(self):
        """
        Returns the ADB tool path
        """
        return self.__adb_path

    def start_server(self):
        """
        Starts the ADB server
        adb start-server
        """
        self.run_cmd('start-server')
        return self.__output

    def kill_server(self):
        """
        Kills the ADB server
        adb kill-server
        """
        self.run_cmd('kill-server')

    def restart_server(self):
        """
        Restarts the ADB server
        """
        self.kill_server()
        return self.start_server()

    def restore_file(self,file_name):
        """
        Restore device contents from the <file> backup archive
        adb restore <file>
        """
        self.run_cmd('restore %s' % file_name)
        return self.__output

    def wait_for_device(self):
        """
        Block operations until device is online
        adb wait-for-device
        """
        self.run_cmd('wait-for-device')
        return self.__output

    def get_help(self):
        """
        Returns ADB help
        adb help
        """
        self.run_cmd('help')
        return self.__output

    def get_devices(self):
        """
        Return a dictionary of connected devices along with an incremented Id.
        adb devices
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
        self.__target = self.__devices[device]
        return "[+] Target device set: %s" % self.get_target_device()

    def get_target_device(self):
        """
        Returns the selected device to work with
        """
        if self.__target == None:
            print "[*] No device target set"

        return self.__target

    def get_state(self):
        """
        Get ADB state. Returns either offline | offline | device
        adb get-state
        """
        return self.run_cmd('get-state')

    def get_model(self):
        """
        Get Model name from taget device
        """
        self.run_cmd("devices -l")
        device_model = ""
        if self.__error is not None:
            return self.__error
        try:
            for line in self.__output.split("\n"):
                if line.startswith(self.__target):
                    pattern = r"model:(.+)\sdevice"
                    pat = re.compile(pattern)
                    device_model = pat.findall(line)
                    device_model = re.sub("[\[\]\'\{\}<>]", '', str(device_model))
        except Exception as e:
            return "[-] Error: %s" %e.args[0]

        return device_model

    def get_serialno(self):
        """
        Get serialno from target device
        adb get-serialno
        """
        return self.run_cmd('get-serialno')

    def reboot_device(self,mode=0):
        """
        Reboot the target device
        Specify mode to reboot normally, recovery or bootloader
        adb reboot <normally (0)/recovery (1) /bootloader (2)>
        """
        if not mode in (self.REBOOT_NORMAL, self.REBOOT_RECOVERY,self.REBOOT_BOOTLOADER):
            self.__error = "mode must be REBOOT_NORMAL/REBOOT_RECOVERY/REBOOT_BOOTLOADER"
            return self.__output

        cmd_str = "reboot"
        if mode == self.REBOOT_RECOVERY:
            cmd_str += " recovery"
        elif mode == self.REBOOT_BOOTLOADER:
            cmd_str += " bootloader"

        return self.run_cmd(cmd_str)

    def set_adb_root(self, mode):
        """
        restarts the adbd daemon with root permissions
        adb root
        """
        return self.run_cmd('root')

    def set_system_rw(self):
        """
        Mounts /system as rw
        adb remount
        """
        self.run_cmd("remount")
        return self.__output

    def get_remote_file(self,remote,local):
        """
        Pulls a remote file
        adb pull remote local
        """
        self.run_cmd('pull \"%s\" \"%s\"' % (remote,local) )
        if "bytes in" in self.__error:
            self.__output = self.__error
            self.__error = None
        return self.__output

    def push_local_file(self,local,remote):
        """
        Push a local file
        adb push local remote
        """
        self.run_cmd('push \"%s\" \"%s\"' % (local,remote) )
        return self.__output

    def shell_command(self,cmd):
        """
        Executes a shell command
        adb shell <cmd>
        """
        self.run_cmd('shell %s' % cmd)
        return self.__output

    def listen_usb(self):
        """
        Restarts the adbd daemon listening on USB
        adb usb
        """
        self.run_cmd("usb")
        return self.__output

    def listen_tcp(self,port=DEFAULT_TCP_PORT):
        """
        Restarts the adbd daemon listening on the specified port
        adb tcpip <port>
        """
        self.run_cmd("tcpip %s" % port)
        return self.__output

    def get_bugreport(self):
        """
        Return all information from the device that should be included in a bug report
        adb bugreport
        """
        self.run_cmd("bugreport")
        return self.__output

    def get_jdwp(self):
        """
        List PIDs of processes hosting a JDWP transport
        adb jdwp
        """
        return self.run_cmd("jdwp")

    def get_logcat(self,lcfilter=""):
        """
        View device log
        adb logcat <filter>
        """
        self.run_cmd("logcat %s" % lcfilter)
        return self.__output

    def run_emulator(self,cmd=""):
        """
        Run emulator console command
        """
        self.run_cmd("emu %s" % cmd)
        return self.__output

    def connect_remote (self,host=DEFAULT_TCP_HOST,port=DEFAULT_TCP_PORT):
        """
        Connect to a device via TCP/IP
        adb connect host:port
        """
        self.run_cmd("connect %s:%s" % ( host , port ) )
        return self.__output

    def disconnect_remote (self , host=DEFAULT_TCP_HOST , port=DEFAULT_TCP_PORT):
        """
        Disconnect from a TCP/IP device
        adb disconnect host:port
        """
        self.run_cmd("disconnect %s:%s" % ( host , port ) )
        return self.__output

    def ppp_over_usb(self,tty=None,params=""):
        """
        Run PPP over USB
        adb ppp <tty> <params>
        """
        if tty is None:
            return self.__output

        cmd = "ppp %s" % tty
        if params != "":
            cmd += " %s" % params

        self.run_cmd(cmd)
        return self.__output

    def sync_directory(self,directory=""):
        """
        Copy host->device only if changed (-l means list but don't copy)
        adb sync <dir>
        """
        self.run_cmd("sync %s" % directory )
        return self.__output

    def forward_socket(self,local=None,remote=None):
        """
        Forward socket connections
        adb forward <local> <remote>
        """
        if local is None or remote is None:
            return self.__output
        self.run_cmd("forward %s %s" % (local,remote) )
        return self.__output

    def uninstall(self,package=None,keepdata=False):
        """
        Remove this app package from the device
        adb uninstall [-k] package
        """
        if package is None:
            return self.__output
        cmd = "uninstall %s" % (package if keepdata is True else "-k %s" % package )
        self.run_cmd(cmd)
        return self.__output

    def install(self,pkgapp=None,fwdlock=False,reinstall=False,sdcard=False):
        """
        Push this package file to the device and install it
        adb install [-l] [-r] [-s] <file>
        -l -> forward-lock the app
        -r -> reinstall the app, keeping its data
        -s -> install on sdcard instead of internal storage
        """

        if pkgapp is None:
            return self.__output

        cmd = "install"
        if fwdlock is True:
            cmd += " -l "
        if reinstall is True:
            cmd += " -r "
        if sdcard is True:
            cmd += " -s "

        self.run_cmd("%s %s" % (cmd , pkgapp) )
        return self.__output

    def find_binary(self,name=None):
        """
        Look for a binary file on the device
        """

        self.shell_command("which %s" % name)

        if self.__output is None: # not found
            self.__error = "'%s' was not found" % name
        elif self.__output.strip() == "which: not found": # which binary not available
            self.__output = None
            self.__error = "which binary not found"
        else:
            self.__output = self.__output.strip()

        return self.__output

#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import traceback

from kindo.utils.logger import Logger
from kindo.utils.args_parser import ArgsParser
from kindo.modules.run_module import RunModule
from kindo.modules.build_module import BuildModule
from kindo.modules.search_module import SearchModule
from kindo.modules.shell_module import ShellModule
from kindo.modules.clean_module import CleanModule
from kindo.modules.register_module import RegisterModule
from kindo.modules.push_module import PushModule
from kindo.modules.images_module import ImagesModule
from kindo.modules.rmi_module import RmiModule
from kindo.modules.info_module import InfoModule
from kindo.modules.version_module import VersionModule
from kindo.modules.help_module import HelpModule
from kindo.modules.pull_module import PullModule
from kindo.modules.commit_module import CommitModule
from kindo.modules.logout_module import LogoutModule
from kindo.modules.login_module import LoginModule
from kindo.modules.rm_module import RmModule


class Kindo:
    def __init__(self, startfolder, argv):
        self.startfolder = startfolder
        self.argv = argv
        self.options, self.configs = ArgsParser(self.argv).parse_args()

        logs_path = "/var/log/kindo" if os.path.isdir("/var/log") else os.path.join(self.startfolder, "logs")
        is_debug = True if "debug" in self.configs else False

        self.logger = Logger(logs_path, is_debug)

        self.core_commands = {
            "run": RunModule,
            "build": BuildModule,
            "search": SearchModule,
            "shell": ShellModule,
            "clean": CleanModule,
            "register": RegisterModule,
            "push": PushModule,
            "images": ImagesModule,
            "rm": RmModule,
            "rmi": RmiModule,
            "info": InfoModule,
            "login": LoginModule,
            "logout": LogoutModule,
            "version": VersionModule,
            "help": HelpModule,
            "pull": PullModule,
            "commit": CommitModule
        }

    def start(self):
        if len(self.argv) <= 1:
            self.show_help()
            return

        command = self.options[1].lower()
        if command not in self.core_commands:
            ext = os.path.splitext(command)[1].lower()
            if ext not in [".kic", ".ki"]:
                self.show_help()
                return
            command = "build" if ext == ".kic" else "run"
            self.options.insert(1, command)

        try:
            core_command_cls = self.core_commands[command](
                self.startfolder,
                self.configs,
                self.options,
                self.logger
            )

            core_command_cls.start()
        except KeyboardInterrupt:
            pass
        except:
            try:
                self.logger.debug(traceback.format_exc())
            except:
                pass

    def show_help(self):
        banner = """a simple tool for packaging and deploying your codes
kindo commands:
    build       Build an image from the kicfile
    commit      Commit local image to the image's path
    clean       Clean the local caches
    help        Show the command options
    images      List local images
    info        Display system-wide information
    login       Account login
    logout      Account logout
    pull        Pull an image from the kindo hub
    push        Push an image to the kindo hub
    register    Register the kindo hub's account
    rm          Delete the owned image in the kindo hub
    rmi         Remove one or more local images
    run         Run image commands to the target operating system
    search      Search an image on the kindo hub
    shell       Execute shell command directly
    version     Show the kindo information

script commands:
    add        Add local or remote file to the target operating system
    addonrun   Add file or directory to the target operating system when running
    centos     Run an shell command on CentOS, others ignore
    check      Check whether the file or port existed or not
    download   Download file from the target operating system
    run        Run an shell command
    ubuntu     Run an shell command on Ubuntu, others ignore
    workdir    set the work directory when the shell command is running
"""
        self.logger.info(banner)


def run():
    startfolder = os.path.dirname(sys.executable)
    if sys.argv[0][-3:] == ".py":
        startfolder = os.path.dirname(os.path.realpath(sys.argv[0]))

    kindo = Kindo(startfolder, sys.argv)
    kindo.start()

if __name__ == '__main__':
    run()

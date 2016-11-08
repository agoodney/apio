# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016 FPGAwars
# -- Author Jesús Arroyo
# -- Licence GPLv2

import json
from os.path import isfile, isdir, join

from apio.util import get_home_dir, get_package_dir


class Profile(object):

    def __init__(self):
        self.config = {}
        self.packages = {}
        self._profile_path = join(get_home_dir(), 'profile.json')
        self.load()

    def check_package(self, name, release_name):
        return (name in self.packages.keys()) or \
               isdir(get_package_dir(release_name))

    def check_package_version(self, name, version, release_name=''):
        ret = False
        if self.check_package(name, release_name):
            pkg_version = self.get_package_version(name, release_name)
            pkg_version = self._convert_old_version(pkg_version)
            version = self._convert_old_version(version)
            ret = (pkg_version < version)
        return ret

    def _convert_old_version(self, version):
        # Convert old versions to new format
        try:
            v = int(version)
            version = '1.{}.0'.format(v)
        except ValueError:
            pass
        return version

    def check_exe_default(self):
        return self.get_config_exe() == 'default'

    def add_package(self, name, version):
        self.packages[name] = {'version': version}

    def add_config(self, exe):
        self.config = {'exe': exe}

    def remove_package(self, name):
        if name in self.packages.keys():
            del self.packages[name]

    def get_package_version(self, name, release_name=''):
        version = '0.0.0'
        if name in self.packages.keys():
            version = self.packages[name]['version']
        elif release_name:
            dir_name = get_package_dir(release_name)
            if isdir(dir_name):
                with open(join(dir_name, 'package.json'), 'r') as json_file:
                    try:
                        tmp_data = json.load(json_file)
                        if 'version' in tmp_data.keys():
                            version = tmp_data['version']
                    except:
                        pass
        return version

    def get_config_exe(self):
        if 'exe' in self.config.keys():
            return self.config['exe']
        else:
            return 'default'

    def load(self):
        data = {}
        if isfile(self._profile_path):
            with open(self._profile_path, 'r') as profile:
                try:
                    data = json.load(profile)
                    if 'config' in data.keys():
                        self.config = data['config']
                    if 'packages' in data.keys():
                        self.packages = data['packages']
                    else:
                        self.packages = data  # Backward compatibility
                except:
                    pass

    def save(self):
        with open(self._profile_path, 'w') as profile:
            data = {'config': self.config, 'packages': self.packages}
            json.dump(data, profile)

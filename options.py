#!/usr/bin/env python3
# coding=UTF8

import logging.config
import sys
import inspect
import argparse
import configparser

class Options(object):

    def __init__(self, parser: argparse.ArgumentParser = None, **kwargs):
        self.opt = None
        self.cfg = None
        self.show_more_args = '--more' in sys.argv
        if parser:
            self.parser = parser
        else:
            self.parser = argparse.ArgumentParser(**kwargs)

    def load_config(self, cfg_file=None):
        """
        Loads config from a given configuration file.

        If a configuration file is not provided then the script will attempt to auto-deduce
        the file based on the name of the file that the function is called from.

        That is, if calling load_config from a file myapp.py the script will attempt to load
        configuration from a corresponding file called myapp.cfg located in the same directory.

        No errors will be thrown if the configuration file does not exist.
        """
        if not cfg_file:
            cfg_file = str.replace(sys.argv[0],'.py','.cfg')

        self.cfg = configparser.ConfigParser()
        with open(cfg_file, 'r') as fp:
            self.cfg.read_file(fp)

        logging.config.fileConfig(cfg_file)

    def load_params(self, class_instance=None, function_name='param_setup'):
        """
        Loads parameters from a given class or object.

        This is meant as a short-hand alternative that allows us to write:
            - opts.load_params(UsefulClass)

        rather than writing:
            - UsefulClass.param_setup(opts.parser)

        This assumes that the function name takes an ArgumentParser object.

        If no class or object is provided then the parameters from the Options class
        are loaded instead.
        """
        if class_instance:
            function = getattr(class_instance, function_name, None)
            if callable(function):
                func_args = inspect.getargspec(function).args
                args = {}
                if 'parser' in func_args:
                    args['parser'] = self.parser
                if 'show_more_args' in func_args:
                    args['show_more_args'] = self.show_more_args
                function(**args)
        else:
            self.prepare_params()


    def prepare_params(self, parser=None):
        """
        Prepares parameters provided by the Options class.
        """

        if not parser:
            parser = self.parser

        parser.add_argument(
            '--more',
            help=argparse.SUPPRESS if self.show_more_args else 'show advanced options',
            action='store_true'
        )

    def parse_args(self, **kwargs):

        self.opt = self.parser.parse_args(**kwargs)

    def print_help(self):

        if self.parser._subparsers is not None and len(sys.argv) > 1:
            for a in self.parser._subparsers._group_actions:
                for choice in a.choices:
                    if choice == sys.argv[1]:
                        a.choices[choice].print_help()
                        return
        self.parser.print_help()

    def get(self, key, default='', value=None, prefix=None, suffix=None):
        """
        Get a configuration value for a given option / key in an nvl manner.

        Output is in the following order of precedence:
            - the provided value if it is not None
            - command line argument value, if provided
            - configuration item, if set
            - default value provided

        This naturally assumes that the argparse destination variables and
        corresponding configuration items have the same names.

        If an optional substitute override prefix is provided then the script will
        return the value of <prefix>_<key> if it exists and fall back to returning
        the value of <key> if not. This can be used to enable project specific
        configuration overrides without changing the logic of the script, as an
        example.

        Similarly if an optional substitute override suffix is provided then the
        script will return the value of <key>_<suffix> if it exists and fall back to
        returning the value of <key> if not. This can be used to enable value
        specific configuration overrides without changing the logic of the script.

        If both a prefix and a suffix is provided then the script will return the
        value of <prefix>_<key>_<suffix> if it exists and fall back to returning
        the value of <prefix>_<key> if it exists. If it does not then it will fall
        back to returning the value of <key>_<suffix> if it exists, and again if not
        then it will fall back to returning the value of <key>. In other words the
        prefix takes precedence over the suffix.
        """

        if value is not None:
            return value

        if prefix is not None:
            return self.get('{0}_{1}'.format(prefix,key), default=self.get(key, default=default, suffix=suffix), suffix=suffix)

        if suffix is not None:
            return self.get('{0}_{1}'.format(key,suffix), default=self.get(key, default=default))

        if type(self.opt) == argparse.Namespace:
            optvars = vars(self.opt)
            if key in optvars and optvars[key] is not None:
                return optvars[key]

        if self.cfg is not None:
            if key in self.cfg['settings'].keys():
                value = self.cfg['settings'][key]
                if type(default) == bool:
                    if value.lower() in ['true', 'on', 'enabled', '1']:
                        return True
                    else:
                        return False

                if type(default) == list:
                    return value.split(',')

                if type(default) == int:
                    return int(value)

                return value

        return default

    def enabled(self, key, default=False, value=None, prefix=None, suffix=None):
        output = self.get(key, default=default, value=value, prefix=prefix, suffix=suffix)
        if type(output) != bool:
            return False

        return output

    def disabled(self, key, default=True, value=None, prefix=None, suffix=None):
        output = self.get(key, default=default, value=value, prefix=prefix, suffix=suffix)
        if type(output) != bool:
            return True

        return not output

    def set(self, key, value):

        exec("self.opt.{0} = value".format(key))

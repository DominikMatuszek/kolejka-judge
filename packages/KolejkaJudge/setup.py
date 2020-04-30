#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

import os
import re
from setuptools import setup, find_packages

def sub_find_packages(module):
    return [ module ] + [ module + '.' + submodule for submodule in find_packages(re.sub(r'\.', r'/', module)) ]

kolejka_judge = {
        'name' : 'KolejkaJudge',
        'description' : 'Kolejka Satori Judge',
        'packages' : sub_find_packages('kolejka.judge'),
        'install_requires' : [
            'setproctitle',
            'pyyaml',
            'KolejkaCommon',
            'KolejkaClient',
        ],
        'entry_points' : {
            'console_scripts' : [
                'kolejka-judge = kolejka.judge:main',
            ],
        },
    }

if __name__ == '__main__':
    assert os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup.cfg'))
    setup(**kolejka_judge)
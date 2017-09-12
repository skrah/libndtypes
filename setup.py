#
# BSD 3-Clause License
#
# Copyright (c) 2017, plures
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from distutils.core import setup, Extension
from distutils.cmd import Command
from glob import glob
import sys, os
import subprocess
import shutil


DESCRIPTION = \
    """Dynamic types for data description and in-memory computations"""


def get_module_path():
    pathlist = glob("build/lib.*/")
    if pathlist:
        return pathlist[0]
    raise RuntimeError("cannot find ndtypes module in build directory")


if len(sys.argv) == 2:
    if sys.argv[1] == 'test':
        module_path = get_module_path()
        python_path = os.getenv('PYTHONPATH')
        path = python_path + ':' + module_path if python_path else module_path
        env = os.environ.copy()
        env['PYTHONPATH'] = path
        ret = subprocess.call([sys.executable, "python/test_ndtypes.py"], env=env)
        sys.exit(ret)
    elif sys.argv[1] == 'clean':
        shutil.rmtree("build", ignore_errors=True)
        os.chdir("python")
        shutil.rmtree("__pycache__", ignore_errors=True)
        sys.exit(0)
    else:
        pass


def ndtypes_ext():
    include_dirs = ["libndtypes"]

    depends = [
      "libndtypes/attr.h",
      "libndtypes/grammar.h",
      "libndtypes/lexer.h",
      "libndtypes/ndtypes.h",
      "libndtypes/parsefuncs.h",
      "libndtypes/seq.h",
      "libndtypes/symtable.h"
    ]

    sources = [
      "python/_ndtypes.c",
      "libndtypes/alloc.c",
      "libndtypes/attr.c",
      "libndtypes/display.c",
      "libndtypes/display_meta.c",
      "libndtypes/equal.c",
      "libndtypes/grammar.c",
      "libndtypes/lexer.c",
      "libndtypes/match.c",
      "libndtypes/ndtypes.c",
      "libndtypes/parsefuncs.c",
      "libndtypes/parser.c",
      "libndtypes/seq.c",
      "libndtypes/symtable.c",
    ]

    if sys.platform == "win32":
        extra_compile_args = [
          "/wd4200", "/wd4201", "/wd4244", "/wd4267", "/wd4702",
          "/wd4127", "/nologo", "/DYY_NO_UNISTD_H=1", "/D__STDC_VERSION__=199901L"
        ]
    else:
        extra_compile_args = [
           "-Wextra", "-Wno-missing-field-initializers", "-std=c11"
        ]

    return Extension (
      "_ndtypes",
      include_dirs=include_dirs,
      extra_compile_args = extra_compile_args,
      depends = depends,
      sources = sources
    )

setup (
    name = "_ndtypes",
    version = "0.1",
    description = DESCRIPTION,
    url = "https://github.com/plures/ndtypes",
    license = "BSD License",
    keywords = ["ndtypes", "array computing", "data description"],
    platforms = ["Many"],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
    ],
    ext_modules = [ndtypes_ext()],
)

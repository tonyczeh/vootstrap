#!/usr/bin/env python
import sys
import textwrap
try:
    import virtualenv  # @UnresolvedImport
except:
    from .lib import virtualenv  # @Reimport

from . import snippits


__version__ = "0.9.1"


def file_search_dirs():
    dirs = []
    for d in virtualenv.file_search_dirs():
        if "vootstrap" not in d:
            dirs.append(d)
    return dirs


def make_parser():
    parser = virtualenv.ConfigOptionParser(
        usage="usage: %prog [OPTIONS] OUTFILE",
        version=__version__,
        formatter=virtualenv.UpdatingDefaultsHelpFormatter())

    parser.add_option(
        "-v", "--verbose",
        action="count",
        dest="verbose",
        default=0,
        help="Increase verbosity")

    parser.add_option(
        "-q", "--quiet",
        action="count",
        dest="quiet",
        default=0,
        help="Decrease verbosity")

    parser.add_option(
        "-p", "--python",
        dest="python",
        metavar="PYTHON_EXE",
        help="The Python interpreter to use, e.g., --python=python2.5 will "
        "use the python2.5 interpreter to create the new environment.  The "
        "default is the interpreter that virtualenv was installed with (%s)"
        % sys.executable)

    parser.add_option(
        "--clear",
        dest="clear",
        action="store_true",
        help="Clear out the non-root install and start from scratch")

    parser.add_option(
        "--no-site-packages",
        dest="no_site_packages",
        action="store_true",
        help="Don't give access to the global site-packages dir to the "
             "virtual environment (default; deprecated)")

    parser.add_option(
        "--system-site-packages",
        dest="system_site_packages",
        action="store_true",
        help="Give access to the global site-packages dir to the "
             "virtual environment")

    parser.add_option(
        "--unzip-setuptools",
        dest="unzip_setuptools",
        action="store_true",
        help="Unzip Setuptools or Distribute when installing it")

    parser.add_option(
        "--relocatable",
        dest="relocatable",
        action="store_true",
        help="Make an EXISTING virtualenv environment relocatable.  "
        "This fixes up scripts and makes all .pth files relative")

    parser.add_option(
        "--distribute",
	"--use-distribute",
        dest="use_distribute",
        action="store_true",
        help="Use Distribute instead of Setuptools. Set environ variable "
        "VIRTUALENV_DISTRIBUTE to make it the default ")

    parser.add_option(
        "--extra-search-dir",
        dest="search_dirs",
        action="append",
        default=['.'],
        help="Directory to look for setuptools/distribute/pip distributions "
        "in. You can add any number of additional --extra-search-dir paths.")

    parser.add_option(
        "--never-download",
        dest="never_download",
        action="store_true",
        help="Never download anything from the network.  Instead, virtualenv "
        "will fail if local distributions of setuptools/distribute/pip are "
        "not present.")

    parser.add_option(
        "--prompt",
        dest="prompt",
        help="Provides an alternative prompt prefix for this environment")

    parser.add_option("--install-requirements",
        default=False,
        action="store_true",
        dest="install_requirements",
        help="Install requirements.txt after vootstrapping")

    parser.add_option(
        "--path",
        action="append",
        dest="path",
        help="Directory to add to vootstrapped sys.path. You can add any "
        "number of additional --path paths. Relative directories are relative "
        "to the vootstrapped directory")

    return parser


def adjust_options(options):
    out_str = "def adjust_options(options, args):\n"
    opts = [
        "verbose",
        "quiet",
        "python",
        "clear",
        "no_site_packages",
        "system_site_packages",
        "unzip_setuptools",
        "relocatable",
        "use_distribute",
        "search_dirs",
        "never_download",
        "prompt"
    ]
    for opt in opts:
        out_str += "    options.%s = %s\n" % (opt, getattr(options, opt))
    out_str += snippits.ADJUST_OPTIONS_ARGS

    return textwrap.dedent(out_str)


def after_install(options):
    if not (options.install_requirements or options.path):
        return ""

    out_str = snippits.AFTER_INSTALL_PREFIX

    if options.path:
        out_str += snippits.AFTER_INSTALL_PATH(options.path)

    if options.install_requirements:
        out_str += snippits.AFTER_INSTALL_REQUIREMENTS

    return textwrap.dedent(out_str)


def vootify(options):
    return virtualenv.create_bootstrap_script(
        adjust_options(options) +
        after_install(options)
    )


def main():
    parser = make_parser()
    (options, args) = parser.parse_args()

    if not len(args):
        parser.print_help()
        return 1

    with open(args[0], "w") as outfile:
        outfile.write(vootify(options))

    return 0


if __name__ == "__main__":
    exit_code = main()
    if exit_code():
        sys.exit(exit_code)

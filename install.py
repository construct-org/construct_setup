from __future__ import print_function
import sys
import platform
import argparse
from subprocess import check_call, check_output, PIPE
import shlex
import os
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen
import logging

# Configure Logging
logging.basicConfig(format='%(levelname)-8s | %(message)s', level=logging.DEBUG)
_log = logging.getLogger('construct_setup')


def log(message):
    print(message)

debug = _log.debug
critical = _log.critical
error = _log.error
info = _log.info
warning = _log.warning


def abort(message):
    critical(message)
    log('Aborting install.')
    sys.exit()


def setup_log_colors():
    '''Borrowed from django.
    https://github.com/django/django/blob/master/django/core/management/color.py
    '''

    supported_platform = (
        sys.platform != 'Pocket PC' and
        (sys.platform != 'win32' or 'ANSICON' in os.environ)
    )

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if supported_platform and is_a_tty:
        logging.addLevelName(logging.WARNING, "\033[1;33mWARNING\033[1;0m")
        logging.addLevelName(logging.ERROR, "\033[1;31mERROR\033[1;0m")
        logging.addLevelName(logging.CRITICAL, "\033[1;31mCRITICAL\033[1;0m")
        logging.addLevelName(logging.DEBUG, "\033[1;41mDEBUG\033[1;0m")
        logging.addLevelName(logging.INFO, "INFO")


# Configure Globals
PLATFORM = platform.system()
DEFAULT_INSTALL_DIR = {
    'Windows': 'C:/construct',
    'Linux': '/usr/local/construct',
    'Mac': '/opt/local/construct'
}[PLATFORM]
VERBOSE = False
PIP_PATH = (
    'git+git://github.com/construct-org/construct_setup.git'
    '@%s#egg=construct_setup'
)


# Utilities
def join_path(*paths):
    return os.path.normpath(os.path.join(*paths)).replace('\\', '/')


def ensure_exists(folder):
    debug('Ensuring that "%s" exists.' % folder)
    if not os.path.exists(folder):
        debug('Creating "%s".' % folder)
        os.makedirs(folder)


def is_available(cmd):
    try:
        check_call(cmd, stdout=PIPE, stderr=PIPE)
        return True
    except:
        return False


def get_latest_release():
    return check_output('git describe --tags').strip()


def run(cmd, abort_on_fail=True, **kwargs):
    try:
        debug('Executing command: %s' % cmd)
        check_call(cmd)
    except:
        if abort_on_fail:
            abort('Failed to execute: %s' % cmd)
        return False


def create_venv(python, env_dir):
    if os.path.exists(env_dir):
        warning('Virtual env already exists.')
        return

    if is_available(python + ' -c "import virtualenv"'):
        run(python + ' -m virtualenv --no-site-packages ' + env_dir)
    elif is_available(python + ' -c "import venv"'):
        run(python + ' -m venv --no-site-packages ' + env_dir)
    else:
        success = run(
            python + ' -m pip install virtualenv',
            abort_on_fail=False
        )
        if success:
            run(python + ' -m virtualenv --no-site-packages ' + env_dir)
        else:
            abort(
                'Failed to setup a virtualenv for construct.\n\n'
                'Install virtualenv for "%s"' % python
            )


def pip_install(python, *args):
    args = [python, '-m', 'pip', 'install'] + list(args)
    run(' '.join(args), abort_on_fail=True)


def move_dir(src, dest):
    import shutil
    shutil.move(src, dest)


def _install_win(version, python, where):

    bin_path = join_path(where, 'bin')
    latest_path = join_path(where, 'latest')
    install_path = join_path(where, version)
    install_packages = join_path(install_path, 'packages')
    install_bin = join_path(install_path, 'bin')
    install_env = join_path(install_path, 'python')
    install_py = join_path(install_env, 'Scripts', 'python.exe')
    pip_path = PIP_PATH % version

    ensure_exists(where)
    ensure_exists(bin_path)
    ensure_exists(install_path)
    create_venv(python, install_env)
    pip_install(
        install_py,
        "-I", PIP_PATH % version,
        '--target=%s' % install_packages
    )
    # move_dir(join_path(install_packages, 'bin'), install_bin)


def _install_linux(version, python, where):
    pass


def _install_mac(version, python, where):
    pass


def install(version, python, where):
    installer = {
        'Windows': _install_win,
        'Linux': _install_linux,
        'Darwin': _install_mac
    }[PLATFORM]
    log('Installing Construct-%s to "%s".' % (version, where))
    debug('Using "%s".' % python)
    installer(version, python, where)


def main():

    setup_log_colors()
    if not is_available('git --version'):
        abort(
            'Git is required to install construct.\n\n'
            'Download it from https://git-scm.com/.'
        )

    parser = argparse.ArgumentParser('construct_installer', add_help=True)
    parser.add_argument(
        '--version',
        required=False,
        action='store',
        default=get_latest_release()
    )
    parser.add_argument(
        '--python',
        action='store',
        help='Python Executable',
        default=sys.executable
    )
    parser.add_argument(
        '--where',
        action='store',
        help='Where to install',
        default=DEFAULT_INSTALL_DIR
    )

    args = parser.parse_args()
    if not is_available(args.python + ' -c "import pip"'):
        abort(
            'pip is required to install construct.\n\n'
            'Get it from https://pip.pypa.io/en/stable/installing/.'
        )

    install(**vars(args))


if __name__ == "__main__":
    main()

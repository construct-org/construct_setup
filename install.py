from __future__ import print_function
import sys
import platform
import argparse
from subprocess import check_call, check_output, PIPE
import os
import re
import shutil
import logging

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    input = raw_input

# Configure Logging
logging.basicConfig(format='%(levelname)-8s | %(message)s', level=logging.DEBUG)
_log = logging.getLogger('construct_setup')


def log(message, *args):
    print(message % args)

debug = _log.debug
critical = _log.critical
error = _log.error
info = _log.info
warning = _log.warning


def abort(message, *args):
    critical(message, *args)
    log('Install Aborted.')
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
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
THIS_BIN = os.path.join(THIS_DIR, 'bin')
PLATFORM = platform.system()
DEFAULT_INSTALL_DIR = {
    'Windows': 'C:/construct',
    'Linux': '/usr/local/construct',
    'Mac': '/opt/local/construct'
}[PLATFORM]
DEFAULT_VERSION = '0.1.23'
DEFAULT_PYTHON = sys.executable
VERBOSE = False
PIP_PACKAGE_PATH = (
    'git+git://github.com/construct-org/construct_setup.git'
    '@%s#egg=construct_setup'
)


# Windows Utilities
def _get_winreg():
    try:
        import _winreg as winreg
    except:
        import winreg
    return winreg


def _get_env_lookup(user=False):
    winreg = _get_winreg()
    user_reg_path = 'Environment'
    reg_path = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    if user:
        return winreg.HKEY_CURRENT_USER, user_reg_path
    else:
        return winreg.HKEY_LOCAL_MACHINE, reg_path


def _win_get_env(name, user=False):
    winreg = _get_winreg()
    root, path = _get_env_lookup(user)

    try:
        with winreg.OpenKey(root, path) as key:
            return winreg.QueryValueEx(key, name)[0]
    except WindowsError:
        return ''


def _win_set_env(name, value, user=False):
    winreg = _get_winreg()
    root, path = _get_env_lookup(user)

    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_ALL_ACCESS) as key:
            try:
                reg_type = winreg.QueryValueEx(key, name)[1]
            except:
                if '%' in value:
                    reg_type = winreg.REG_EXPAND_SZ
                else:
                    reg_type = winreg.REG_SZ
            winreg.SetValueEx(key, name, 0, reg_type, value)
            return True
    except WindowsError:
        return False


def _send_wm_settingchange(path):
    import ctypes
    from ctypes.wintypes import HWND, UINT, WPARAM, LPARAM, LPVOID
    send_message = ctypes.windll.user32.SendMessageW
    send_message.argtypes = HWND, UINT, WPARAM, LPVOID
    send_message.restype = LPARAM
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    send_message(HWND_BROADCAST, WM_SETTINGCHANGE, 0, path)


# Utilities
def join_path(*paths):
    return os.path.normpath(os.path.join(*paths)).replace('\\', '/')


def is_elevated():
    return bool(int(os.environ.get('SCRIM_ADMIN', 0)))


def execute_after(cmd):
    script = os.environ.get('SCRIM_PATH')
    if script:
        with open(script, 'a') as f:
            f.write(cmd + '\n')


def ensure_exists(folder):
    debug('Ensuring that "%s" exists.', folder)
    if not os.path.exists(folder):
        debug('Creating "%s".', folder)
        os.makedirs(folder)


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def is_available(cmd):
    try:
        check_call(cmd, stdout=PIPE, stderr=PIPE, shell=True)
        return True
    except:
        return False


def run(cmd, abort_on_fail=True, **kwargs):
    try:
        debug('Executing command: %s', cmd)
        check_call(cmd)
        return True
    except:
        if abort_on_fail:
            abort('Failed to execute: %s', cmd)
        return False


def get_python_version(python):
    return check_call('python -c "import sys; print(sys.version[:3])"')


def create_venv(python, env_dir, env_py):
    if os.path.exists(env_dir):
        warning('Virtual env already exists.')
        return

    if is_available(python + ' -c "import virtualenv"'):
        run(python + ' -m virtualenv --no-site-packages ' + env_dir)
    elif is_available(python + ' -c "import venv"'):
        run(python + ' -m venv ' + env_dir)
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
                'Install virtualenv for "%s"',
                python
            )

    # Upgrade pip
    debug('Upgrading pip...')
    pip_install(env_py, '-U', 'pip')


def pip_install(python, *args):
    args = [python, '-m', 'pip', 'install'] + list(args)
    run(' '.join(args), abort_on_fail=True)


def move_dir(src, dest):
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.move(src, dest)


def update_symlink(src, dest):

    debug('Updating latest symlink %s > %s.', src, dest)

    if PLATFORM == 'Windows':
        src = os.path.normpath(src)
        dest = os.path.normpath(dest)
        if os.path.isdir(dest):
            run('cmd.exe /C rmdir %s' % dest)
        run('cmd.exe /C mklink /D %s %s' % (dest, src))
    else:
        if os.path.isdir(dest):
            os.remove(dest)
        os.symlink(src, dest)


def copy_scripts(dest):
    debug('Installing scripts to %s', dest)
    construct_bat = join_path(THIS_BIN, 'construct.bat')
    shutil.copy2(construct_bat, dest)
    shutil.copy2(construct_bat, join_path(dest, 'cons.bat'))
    shutil.copy2(join_path(THIS_BIN, 'construct.ps1'), dest)
    shutil.copy2(join_path(THIS_BIN, 'construct.sh'), dest)


def write_pth(site, lib, bin):
    lib_path = os.path.relpath(lib, site).replace('\\', '/')
    bin_path = os.path.relpath(bin, site).replace('\\', '/')
    site_path = join_path(site, 'construct.pth')
    with open(site_path, 'w') as f:
        f.write(lib_path)
        f.write(bin_path)


def update_profile(bash_profile_path, export_cmd, source_cmd, config_cmd=None):
    '''Update bash profile on Linux and MacOS'''

    touch(bash_profile_path)

    with open(bash_profile_path, 'r') as f:
        bash_profile = f.read()

    changed = False
    if export_cmd not in bash_profile:
        bash_profile += '\n' + export_cmd + '\n'
        changed = True
    if source_cmd not in bash_profile:
        bash_profile += source_cmd + '\n'
        changed = True
    if config_cmd:
        match = re.search(r'export CONSTRUCT_CONFIG.*', bash_profile, re.M)
        if not match:
            bash_profile += export_cmd + '\n'
        else:
            string = match.group(0)
            bash_profile = bash_profile.replace(string, export_cmd)
        changed = True
    if changed:
        info('Updating %s', bash_profile_path)
        # TODO: uncomment this bit once this is tested properly
        # with open(bash_profile_file, 'w) as f:
        #     f.write(baseh_profile)
        pass


def install(version, python, where, config):

    if not is_elevated() and PLATFORM == 'Windows':
        log(
            'To fully install Construct you need Admin priviledges. The '
            'following features will be disabled.\n\n'
            '    - Setting system environment variables\n'
        )
        answer = input('Would you like to install anyway? [y] or n\n')
        if answer and answer.lower().startswith('n'):
            log('Abort.')
            sys.exit()

    where = os.path.abspath(where)
    if config:
        config = os.path.abspath(config)

    log('Installing Construct-%s to "%s".', version, where)
    debug('Using "%s".', python)

    # Setup our paths
    pip_package_path = PIP_PACKAGE_PATH % version
    install_path = join_path(where, version)
    install_lib = join_path(install_path, 'lib')
    install_bin = join_path(install_path, 'bin')
    install_env = join_path(install_path, 'python')

    if PLATFORM == 'Windows':
        install_py = join_path(install_env, 'Scripts', 'python.exe')
        install_site = join_path(install_env, 'lib', 'site-packages')
    else:
        pyver = 'python' + get_python_version(python)
        install_py = join_path(install_env, 'bin', 'python')
        install_site = join_path(install_env, 'lib', pyver, 'site-packages')

    # Make sure our install locations exist
    ensure_exists(where)
    ensure_exists(install_path)

    # Create a python virtualenv
    create_venv(python, install_env, install_py)

    # Add a pth file extending the virtualenv to include lib and bin paths
    write_pth(install_site, install_lib, install_bin)

    # Install construct and all of it's dependencies
    pip_install(
        install_py,
        "-I", pip_package_path,
        '--target=%s' % install_lib
    )

    # Move the target bin to the root of the install directory
    move_dir(join_path(install_lib, 'bin'), install_bin)

    # Copy the construct shim files to the installs root directory
    copy_scripts(where)

    # Symlink to the version we just installed
    update_symlink(install_path, join_path(where, 'latest'))

    # Post install
    # Setup system-wide access and activate construct in parent shells.
    if PLATFORM == 'Windows':

        # Modify system PATH to include construct install directory
        info('Adding %s to system PATH' % where)
        system_path = _win_get_env('PATH')
        if where not in system_path.split(';'):
            if is_elevated():
                execute_after('setx /M PATH "%s;%s"' % (where, system_path))

        execute_after('set "PATH=%s;%%PATH%%"' % where)
        if config:
            info('Setting CONSTRUCT_CONFIG to %s' % config)
            if is_elevated():
                execute_after('setx /M CONSTRUCT_CONFIG "%s"' % config)
            execute_after('set "CONSTRUCT_CONFIG=%s"' % config)

    else:

        export_cmd = 'export PATH=%s:$PATH' % where
        source_cmd = 'source %s/construct.sh' % where
        config_cmd = None
        if config:
            config_cmd = 'export CONSTRUCT_CONFIG=%s' % config

        if is_elevated():
            bash_profile_path = '/etc/profile'
        else:
            bash_profile_path = os.path.expanduser('~/.bash_profile')

        # Update bash profile to make sure that each time a user logs in
        # they have access to construct.
        update_profile(bash_profile_path, export_cmd, source_cmd, config_cmd)

        info('Adding %s to PATH' % where)
        execute_after(export_cmd)
        info('Sourcing construct.sh')
        execute_after(source_cmd)
        if config:
            info('Setting CONSTRUCT_CONFIG to %s' % config)
            execute_after(config_cmd)

    info('Install complete!')
    log('\nYou should now have access to the construct cli.\n')
    log('    cons -h')


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
        default=DEFAULT_VERSION
    )
    parser.add_argument(
        '--python',
        action='store',
        help='Python Executable',
        default=DEFAULT_PYTHON
    )
    parser.add_argument(
        '--where',
        action='store',
        help='Where to install',
        default=DEFAULT_INSTALL_DIR
    )
    parser.add_argument(
        '--config',
        action='store',
        help='Location of a construct configuration file.',
        default=''
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

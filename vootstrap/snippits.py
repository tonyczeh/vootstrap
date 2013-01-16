AFTER_INSTALL_PREFIX = """
def after_install(options, home_dir):
    import platform
    import subprocess
    import sys
    import os.path


    abs_home_dir = os.path.abspath(home_dir)
    if sys.platform == "win32":
        pip_path = os.path.join(abs_home_dir, "Scripts", "pip")
        pth_path = os.path.join(
            abs_home_dir,
            "Lib",
            "site-packages",
            "vootstrap.pth"
        )
    else:
        pip_path = os.path.join(abs_home_dir, "bin", "pip")
        pth_path = os.path.join(
            abs_home_dir,
            "lib",
            py_version,
            "site-packages",
            "vootstrap.pth"
        )
"""


AFTER_INSTALL_REQUIREMENTS = """
    requirements = os.path.join(home_dir, "requirements.txt")
    if os.path.exists(requirements):
        subprocess.call(
            [pip_path, "install" , "-r", "requirements.txt", "--upgrade"])
"""


def AFTER_INSTALL_PATH(path):
    return """
    paths = [os.path.join(abs_home_dir, p) for p in %s]
    with open(pth_path, "w") as pth:
        pth.write("\\n".join(paths))
""" % str(path)


ADJUST_OPTIONS_ARGS = """
    try:
        args[0] = "."
    except IndexError:
        args.append(".")
"""

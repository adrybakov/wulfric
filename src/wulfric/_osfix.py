import sys


def _winwait():
    r"""
    Add "Press Enter to continue" behavior to Windows.

    Its a hotfix for Window`s pop-up terminal, which tends to close immediately
    after the script is finished.
    """
    if sys.platform == "win32":
        input("Press Enter to continue")

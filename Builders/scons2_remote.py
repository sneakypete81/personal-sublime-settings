import os
import sys
import argparse
import subprocess

def launch(asic_winpath, sconscript_path, target, server, gui):
    cmd = "cd %s;" % sconscript_path
    cmd += " scons2 %s" % target
    if gui:
        cmd += " --gui"

    cmd = ["vsim"]

    proc = subprocess.Popen(["c:\\cygwin64\\bin\\ssh.exe", "-Y", server, cmd],
                            stdout=subprocess.PIPE)
    # Read each line back on the fly, translating the ERROR paths
    while True:
        line = proc.stdout.readline()
        if not line:
            break

        line = line.replace("** Error: ", "** Error: %s/" % asic_winpath)
        sys.stdout.write(line)

def find_sconscript_path(source_file):
    """Search for a SConscript2 file closest to source_file"""
    path = os.path.dirname(source_file)
    while path:
        if os.path.exists(os.path.join(path, "SConscript2")):
            return path
        # Go up a level
        path = os.path.dirname(path)

    raise OSError("Couldn't find SConscript2 file anywhere above %s" % source_file)

parser = argparse.ArgumentParser(description="Launch scons2 on a remote server")
parser.add_argument("source_file", help="File to compile/simulate")
parser.add_argument("--server", default="elara", help="Remote server to use")
parser.add_argument("--compile_only", action="store_true", help="Just compile, don't run the simulation")
parser.add_argument("--gui", action="store_true", help="Run the simulation in a GUI")
args = parser.parse_args()

# Extract the path to the asic directory (Windows)
asic_winpath = "".join(args.source_file.partition("asic")[:2])

# Search for the SConscript closest to source_file
sconscript_path_win = find_sconscript_path(args.source_file)
sconscript_path = sconscript_path_win.replace(os.path.sep, "/").replace("W:", "work")

if args.compile_only:
    target = "compile"
else:
    target = os.path.splitext(os.path.basename(args.source_file))[0]

launch(asic_winpath, sconscript_path, target, args.server, args.gui)
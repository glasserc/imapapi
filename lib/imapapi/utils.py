import os.path

# Stolen from Stack Overflow http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def is_exe(fpath):
    return os.path.exists(fpath) and os.access(fpath, os.X_OK)

def which(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def fill_template(srcfile, destfile, vars):
    template = open(srcfile)
    conffile = open(destfile, "w")

    data = template.read()

    keys = vars.keys()

    # Replace longer keys first, otherwise we'll replace WHOAMI in WHOAMI_GROUP
    keys.sort(key = len, reverse=True)

    for key in keys:
        data = data.replace(key, vars[key])

    conffile.write(data)
    conffile.close()

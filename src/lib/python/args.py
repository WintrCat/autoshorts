from sys import argv

def parse_args():
    kwargs = {}
    for i, arg in enumerate(argv):
        if arg.startswith("--"):
            try:
                next_arg = argv[i + 1]
            except:
                break
            
            if next_arg.startswith("--"):
                kwargs.update({ arg[2:]: True })
            else:
                kwargs.update({ arg[2:]: next_arg })
    return kwargs
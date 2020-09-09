from . import version

def commands(downloader=None):
    """ Default command
    """
    if len(sys.argv) == 1:
        if downloader is not None:
            downloader()
    else:
        if sys.argv[1] == 'version-check':
            with open('WAPT' + os.sep + 'control', 'r') as control:
                for line in control:
                    if line.startswith('name'):
                        control_name = line.split(':')[1].strip()
                    if line.startswith('version'):
                        control_version = line.split(':')[1].split('-')[0].strip()

            print('Current {} version: {}'.format(control_name, control_version))

            latest_version = latest()
            print(' Latest {} version: {}'.format(latest_version))

            if control_version != latest_version:
                print('New version available, please upgrade package')

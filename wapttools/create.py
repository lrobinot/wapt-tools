import re
import os
import sys
import shutil
import gitlab
import random
from pkg_resources import resource_string

badge = '[![{text} status]({url}/wapt/packages/{package}/badges/{branch}/pipeline.svg?key_text={text})]({url}/wapt/packages/{package}/-/pipelines?&ref={branch}'

def creator(package, verbose=False):
    gl = gitlab.Gitlab.from_config()
    if verbose:
        print("Gitlab url: {}".format(gl.url))

    package_name = os.path.basename(package)
    package_folder = os.path.dirname(package)

    # Check if project exists
    projects = gl.projects.list(search=package_name)
    if len(projects) > 0:
        for project in projects:
            if project.name == package_name:
                if verbose:
                    print('*** ERROR: project {} already exists, aborting.'.format(package_name))
                sys.exit(1)

    if os.path.isdir(package_folder):
        os.makedirs(package_folder)

    if os.path.isdir(package):
        if verbose:
            print('*** ERROR: folder {} already exists, aborting.'.format(package))
        sys.exit(1)

    wapt_group = gl.groups.list(search='wapt')[0]
    packages_group = wapt_group.subgroups.list(search='packages')[0]
    project = gl.projects.create({'name': package_name, 'namespace_id': packages_group.id})

    if package_folder != '':
        os.chdir(package_folder)
    command = 'git clone {}:wapt/packages/{}'.format(gl.url.replace('https://', 'git@'), package_name)
    if verbose:
        print("* {}".format(command))
    os.system(command)
    os.chdir(package_name)

    with open('README.md', 'w') as file:
        file.write('# WAPT {} package\n'.format(package_name))
        file.write('\n')
        file.write(badge.format(text='PROD', branch='master', url=gl.url, package=package_name))
        file.write(badge.format(text='DEV', branch='develop', url=gl.url, package=package_name))

    os.system('git add -A')
    os.system('git commit -m "Add README.md" README.md')
    os.system('git push')

    os.system('git flow init -d')

    os.mkdir('.vscode')
    with open(os.path.join('.vscode', 'extensions.json'), 'w') as file:
        file.write(resource_string('wapttools.data', 'vscode_extensions.json'))

    with open(os.path.join('.vscode', 'launch.json'), 'w') as file:
        file.write(resource_string('wapttools.data', 'vscode_launch.json'))

    with open(os.path.join('.vscode', 'settings.json'), 'w') as file:
        file.write(resource_string('wapttools.data', 'vscode_settings.json'))

    os.mkdir('WAPT')
    with open(os.path.join('WAPT', 'control'), 'w') as file:
        file.write(resource_string('wapttools.data', 'wapt_control').format(url=gl.url, package=package_name))

    os.mkdir('config')
    open(os.path.join('config', '.gitkeep'), 'a').close()

    os.mkdir('sources')
    with open(os.path.join('sources', '.gitignore'), 'w') as file:
        file.write('*\n')
        file.write('!.gitignore\n')

    with open('.editorconfig', 'w') as file:
        file.write(resource_string('wapttools.data', 'dot.editorconfig'))

    with open('.env', 'w') as file:
        file.write('PYTHONHOME=C:\\Program Files (x86)\\wapt\n')
        file.write('PYTHONPATH=C:\\Program Files (x86)\\wapt\n')

    with open('.gitignore', 'w') as file:
        file.write('# Ignore genrated files\n')
        file.write('*.pyc\n')
        file.write('WAPT/certificate.crt\n')
        file.write('WAPT/*.sha256\n')
        file.write('WAPT/wapt.psproj\n')

    with open('.gitlab-ci.yml', 'w') as file:
        file.write('include:\n')
        file.write('  - project: \'wapt/packages/template\'\n')
        file.write('    file: \'/ci/build.yml\'\n')

    with open('version-check.json', 'w') as file:
        file.write(resource_string('wapttools.data', 'version-check.json'))

    script = resource_string('wapttools.data', 'setup.tmpl')
    with open('setup.py', 'w') as file:
        file.write(script)

    os.system('git add .')
    os.system('git commit -m "Skeleton" -a')

    os.system('git push --all')

    # Create schedule named AutoVersionChecker
    scheds = project.pipelineschedules.list()
    found = False
    for sched in scheds:
        if sched.description == 'AutoVersionChecker':
            found = True

    if not found:
        sched = project.pipelineschedules.create({
            'ref': 'develop',
            'description': 'AutoVersionChecker',
            'cron_timezone': 'Europe/Paris',
            'cron': '{} 5 * * *'.format(random.randint(0, 59)),
            'active': True
        })

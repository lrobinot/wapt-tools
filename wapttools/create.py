import re
import os
import sys
import shutil
import gitlab
import random
from pkg_resources import resource_string

data_vscode_extensions_json = '''{
  "recommendations": [
    "editorconfig.editorconfig",
    "wayou.vscode-todo-highlight",
    "ms-python.python"
  ]
}
'''

data_vscode_launch_json = '''{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "WAPT: install",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "install",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal",
      "linux": {
        "sudo": true
      },
      "osx": {
        "sudo": true
      }
    },
    {
      "name": "WAPT: remove",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "remove",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal",
      "linux": {
        "sudo": true
      },
      "osx": {
        "sudo": true
      }
    },
    {
      "name": "WAPT: session-setup",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "session-setup",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal"
    },
    {
      "name": "WAPT: -i build upload",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "-i",
        "build-upload",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal",
      "linux": {
        "sudo": true
      },
      "osx": {
        "sudo": true
      }
    },
    {
      "name": "WAPT: uninstall",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "uninstall",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal",
      "linux": {
        "sudo": true
      },
      "osx": {
        "sudo": true
      }
    },
    {
      "name": "WAPT: audit",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "audit",
        "-f",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal",
      "linux": {
        "sudo": true
      },
      "osx": {
        "sudo": true
      }
    },
    {
      "name": "WAPT: update-package-sources",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "update-package-sources",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal",
      "linux": {
        "sudo": true
      },
      "osx": {
        "sudo": true
      }
    },
    {
      "name": "WAPT: upgrade",
      "type": "python",
      "request": "launch",
      "program": "${config:python.wapt-get}",
      "args": [
        "upgrade",
        "-f",
        "${workspaceFolder}"
      ],
      "console": "integratedTerminal",
      "linux": {
        "sudo": true
      },
      "osx": {
        "sudo": true
      }
    }
  ]
}
'''

data_vscode_settings_json = '''{
  "python.wapt-get": "${config:python.pythonPath}/../wapt-get.py",
  "python.pythonPath": "C:\\Program Files (x86)\\wapt\\waptpython.exe",
  "python.linting.enabled": false,
  "python.linting.flake8Enabled": false,
  "editor.rulers": [
    120
  ],
  "todohighlight.include": [
    "*.*"
  ]
}
'''

data_wapt_control = '''package           : geovar-{package}
name              : ** enter name of the package **
version           : 0.0.0-0
architecture      : x64
section           : base
maintainer        : Geovariances IT Service (sysadmin@geovariances.com)
description       :
description_fr    :
description_es    :
description_pt    :
depends           :
conflicts         :
maturity          : BETA
locale            :
target_os         : windows
min_os_version    : 6.1
min_wapt_version  : 1.8
sources           : {url}/wapt/packages/{package}.git
installed_size    :
impacted_process  :
audit_schedule    : 60
editor            :
licence           :
keywords          :
homepage          :
changelog         :
'''

data_editorconfig = '''root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.ini]
end_of_line = crlf

[*.bat]
end_of_line = crlf

[*.py]
indent_size = 4
'''

data_version_check = '''{
  "url_version": "https://.../version-history",
  "html": true,
  "selector": "h6:nth-of-type(1)",
  "cleaners": [
    {
      "pattern": "v([0-9.]*).*",
      "rewrite": "\\1"
    }
  ],
  "url_downloads": "https://.../builds",
  "url_download_file": "https://download.../{version}.exe"
}
'''


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
        file.write('[![PROD status]({url}/wapt/packages/{package}/badges/master/pipeline.svg?key_text=PROD)]({url}/wapt/packages/{package}/-/pipelines?&ref=master)\n'.format(url=gl.url, package=package_name))
        file.write('[![DEV status]({url}/wapt/packages/{package}/badges/develop/pipeline.svg?key_text=DEV)]({url}/wapt/packages/{package}/-/pipelines?&ref=develop)\n'.format(url=gl.url, package=package_name))

    os.system('git add -A')
    os.system('git commit -m "Add README.md" README.md')
    os.system('git push')

    os.system('git flow init -d')

    os.mkdir('.vscode')
    with open(os.path.join('.vscode', 'extensions.json'), 'w') as file:
        file.write(data_vscode_extensions_json)

    with open(os.path.join('.vscode', 'launch.json'), 'w') as file:
        file.write(data_vscode_launch_json)

    with open(os.path.join('.vscode', 'settings.json'), 'w') as file:
        file.write(data_vscode_settings_json)

    os.mkdir('WAPT')
    with open(os.path.join('WAPT', 'control'), 'w') as file:
        file.write(data_wapt_control.format(url=gl.url, package=package_name))

    os.mkdir('config')
    open(os.path.join('config', '.gitkeep'), 'a').close()

    os.mkdir('sources')
    with open(os.path.join('sources', '.gitignore'), 'w') as file:
        file.write('*\n')
        file.write('!.gitignore\n')

    with open('.editorconfig', 'w') as file:
        file.write(data_editorconfig)

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
        file.write(data_version_check)

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

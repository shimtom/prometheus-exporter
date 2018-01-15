#!/usr/bin/env python3

# Description: users metrics from ntpq -np.
# Author: Ben Kochie <superq@gmail.com>

import subprocess


def get_output(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        return None
    return output.decode()


def timestamp(arg):
    # TODO: implement converting arg to timestamp
    return 0


def who():
    users = {}
    result = get_output(['who'])
    for l in result.split('\n'):
        if len(l) > 0:
            username, line = l.split()[:2]
            login_time = l.split()[2:]
            users.setdefault(username, []).append({
                'line': line,
                'timestamp': timestamp(login_time)
            })

    result.split('\n')

    with open('/etc/passwd', 'r') as f:
        for l in f:
            username = l.split(':')[0]
            users.setdefault(username, [])

    print('# HELP user_login login user')
    for username, value in users.items():
        for v in value:
            print('user_login{username="%s",line="%s"} 1 %d' % (
                username, v['line'], v['timestamp']))


# Main function
def main():
    who()


if __name__ == "__main__":
    main()

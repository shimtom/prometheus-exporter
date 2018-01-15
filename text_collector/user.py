#!/usr/bin/env python3

# Description: users metrics.
# TODO: cpu info per user
# TODO: memory info per user
# TODO: process info per user

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
    result = get_output(['who', '-H']).split('\n')
    header = result[0].split()
    for l in result[1:]:
        if len(l) > 0:
            splitted = l.split()[:2]
            username, line = splitted[:2]
            if len(header) == 3:
                login_time = splitted[2:]
            else:
                login_time = splitted[2:-1]
                comment = splitted[-1]

            users.setdefault(username, []).append({
                'line': line,
                'timestamp': timestamp(login_time),
                'comment': comment or ''
            })

    with open('/etc/passwd', 'r') as f:
        for l in f:
            username = l.split(':')[0]
            users.setdefault(username, [])

    print('# HELP node_login_user login user')
    for username, value in users.items():
        for v in value:
            print('node_login_user{username="%s",line="%s",comment="%s"} 1 %d' % (
                username, v['line'], v['comment'], v['timestamp']))


# Main function
def main():
    who()


if __name__ == "__main__":
    main()

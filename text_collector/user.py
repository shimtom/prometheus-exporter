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


def who():
    users = {}
    result = get_output(['who', '-H']).split('\n')
    header = result[0].split()
    for l in result[1:]:
        if len(l) > 0:
            splitted = l.split()
            username, line = splitted[:2]
            login_time = splitted[2:-1]
            comment = None
            if len(header) == 3:
                login_time.append(splitted[-1])
            else:
                comment = splitted[-1]

            users.setdefault(username, []).append({
                'line': line,
                'time': ' '.join(login_time),
                'comment': comment or ''
            })

    with open('/etc/passwd', 'r') as f:
        for l in f:
            username = l.split(':')[0]
            users.setdefault(username, [])

    print('# HELP node_login_user_info login user information')
    s = 'node_login_user_info{username="%s",line="%s",comment="%s",time="%s"} 1'
    for username, value in users.items():
        for v in value:
            print(s % (username, v['line'], v['comment'], v['time']))


# Main function
def main():
    who()


if __name__ == "__main__":
    main()

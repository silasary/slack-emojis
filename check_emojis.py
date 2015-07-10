#!/usr/bin/python3

import os
import argparse
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')


SLACK_URL = 'https://{slack}.slack.com/api/emoji.list?token={token}'


def download_image(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)


def reconcile_aliases(image_url, emoji):
    if image_url.startswith('alias:'):
        image_url = emoji.get(image_url[6:], None)
    return image_url


def main(args):
    r = requests.get(SLACK_URL.format(slack=args.slack, token=args.token))
    if r.status_code == 200:
        emoji = r.json().get('emoji', {})
        if emoji and not os.path.isdir(args.output):
            os.mkdir(args.output)
        names = [image_name for image_name, image_url in emoji.items()]
        files = [ f for f in os.listdir(args.output) if os.path.isfile(os.path.join(args.output,f)) ]
        for emojifile in files:
            if (not os.path.splitext(emojifile)[0] in names):
                print(emojifile + " missing.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('slack', help='name of your slack group.')
    parser.add_argument('token', help='auth token for slack.')
    parser.add_argument('-o', '--output', help='output location of images',
                        default=os.getcwd())
    args = parser.parse_args()
    main(args)

import re
from functions import *


def json_upload(env, start_response):
    """Json upload path"""
    diff_id = '/'.join(env.get('PATH_INFO', '').split('/')[3:-1])
    diff_side = env.get('PATH_INFO', '').split('/')[-1]

    try:
        length = int(env.get('CONTENT_LENGTH', '0'))
    except ValueError:
        start_response('400 BAD REQUEST', [('Content-Type', 'text/html')])
        return ["Zero length request body".encode('utf8')]

    body = env['wsgi.input'].read(length)

    uploaded_content = json_saver(body, diff_id + '_' + diff_side)
    if uploaded_content['status'] != 'success':
        start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'text/html')])
        return [uploaded_content['message'].encode('utf8')]

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [uploaded_content['message'].encode('utf8')]


def json_compare(env, start_response):
    """Json compare path"""
    diff_id = env.get('PATH_INFO', '').split('/')[-1]
    json_comparison = json_diff(diff_id)
    if json_comparison['status'] != 'success':
        start_response('500 INTERNAL SERVER ERROR', [('Content-Type', 'text/html')])
        return [json_comparison['message'].encode('utf8')]

    start_response('200 OK', [('Content-Type', 'text/html')])
    return [str(json_comparison['output']).encode('utf8')]


def index(env, start_response):
    """Index page"""
    start_response('200 OK', [('Content-Type', 'text/html')])


def not_found(env, start_response):
    """Called if no URL matches."""
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
    return ['Not Found']

urls = [
    (r'^$', index),
    (r'^v1/diff/[A-Za-z0-9]+/(left|right)$', json_upload),
    (r'^v1/diff/[A-Za-z0-9]+?$', json_compare)
]


def application(env, start_response):
    """App module"""
    path = env.get('PATH_INFO', '').lstrip('/')
    for regex, callback in urls:
        match = re.search(regex, path)
        if match is not None:
            env['app.url_args'] = match.groups()
            return callback(env, start_response)
    return not_found(env, start_response)


def main():
    print "This is a wsgi app"

if __name__ == "__main__":
    main()
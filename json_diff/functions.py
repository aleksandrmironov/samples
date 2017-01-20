from base64 import b64decode
import json
import os


def json_saver(content, id):
    """Content decoding and json saving"""

#   Decode incoming content
    try:
        json_content = b64decode(content)
    except Exception as error:
        return {'status': 'failure', 'message': 'Unable to decode base64: %s' % str(error), 'output': None}

#   Check if JSON is valid
    try:
        json.loads(json_content)
    except Exception as error:
        return {'status': 'failure', 'message': 'Unable to parse json content: %s' % str(error), 'output': None}

#   Check if we can write JSON content to file
    try:
        f = open(os.path.join('upload', '%s.json' % id), "w")
        f.write(json_content)
        f.close()
    except Exception as error:
        return {'status': 'failure', 'message': 'Unable to write json content to file: %s' % str(error), 'output': None}

    return {'status': 'success', 'message': 'json %s decoded and uploaded' % id, 'output': None}


def json_diff(id):
    """Compare left and right jsons saved previously"""

#   Read saved JSONs
    jsons = {}
    for side in ['left', 'right']:
        if not os.path.isfile('upload/%s_%s.json' % (id, side)):
            return {'status': 'failure', 'message': '%s json for %s does not exist' % (id, side), 'output': None}

        try:
            f = open(os.path.join('upload', '%s_%s.json' % (id, side)))
            json_file_content = f.read()
            json.loads(json_file_content)
            jsons[side] = str(json_file_content)
        except Exception as error:
            return {'status': 'failure', 'message': 'Unable to read json from %(id)s_%(side)s.json: %(error)s' % {'id': id, 'side': side, 'error': str(error)}, 'output': None}

        jsons[side] = json_file_content

    insight = {}
#   IF length is equal
    if len(jsons['left']) == len(jsons['right']):
        length = 0
        offset_length_map = {}
        for offset in range(len(jsons['left'])):
            if jsons['left'][offset] != jsons['right'][offset]:
                length += 1
            else:
                if length > 0:
                    offset_length_map[offset - length] = length
                length = 0

        insight['SameSize'] = 'True'

#       IF JSONs are completely same
        if len(offset_length_map) == 0:
            insight['Equal'] = 'True'
            insight['Diff'] = 'None'

        else:
            insight['Equal'] = 'False'
            insight['Diff'] = []
            for key in sorted(offset_length_map.iterkeys()):
                insight['Diff'].append({'Offset': key, 'Length': offset_length_map[key]})

#   IF length is not equal
    else:
        insight['Equal'] = 'Flase'
        insight['SameSize'] = 'False'
        insight['Diff'] = 'Not applicable'

    return {'status': 'success', 'message': 'jsons %s compared' % id, 'output': json.dumps(insight)}

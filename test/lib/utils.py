import json

def jsonify(result, format=False):
    ''' format JSON output (uncompressed or uncompressed) '''
    if result is None:
        return "{}"
    result2 = result.copy()
    for key, value in result2.items():
        if type(value) is str:
            result2[key] = value.decode('utf-8', 'ignore')
    if format:
        return json.dumps(result2, sort_keys=True, indent=4)
    else:
        return json.dumps(result2, sort_keys=True)

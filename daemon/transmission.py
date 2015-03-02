import request
import json

class transmission(object):

    def __init__(self, host='localhost', port='9091'):

        self.TORRENT_ADD = 'torrent-add'
        self.URI_SCHEME = 'http'
        self.BASE_URL = '%s://%s:%s/transmission/rpc' % (self.URI_SCHEME,
                host, port)

    def add_torrent(self, torrent_file, **kwargs):
        kwargs['filename'] = torrent_file
        kwargs['method'] = self.TORRENT_ADD
        response = self.__submit(kwargs)


    def __submit(self, request_dict):
        try:
            response = request.post(self.BASE_URL,
                    data=json.dumps(request_dict)
            response = json.load(response.text)
            result = {'result': json_response['result']

        except Exception as ex:
            result = {'result': 'failed', 'reason': ex.message,
                'error': str(ex)}
        finally:
            return result




    def status(self):
        return 'This is a text document'

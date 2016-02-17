import json
import urllib.request
import requests


def get_json(url):
    """
    Function that retrieves a json from a given url.
    :return: the json that was received
    """

    with urllib.request.urlopen(url) as response:
        data = response.readall().decode('utf-8')
        data = json.loads(data)
    return data


class ApiObject(object):
    """
    Base mapping class for api objects.
    """

    actions = {}
    base_url = ''

    def create_action(self, action):
        """
        Function that creates a request function based on an action element
        :param action: a dict containing the action parameters
        :return: a function that will make a request with the action parameters
        """

        def f(args=None):
            resp = requests.request(action['method'], self.base_url + action['href'],
                                    json=None if not args else args.json())
            return resp.json()
        return f

    def register_actions(self, data):
        """
        Function that creates action methods for all action elements given
        :param data: a dict containing a '_links' dictionary
        """

        for action in data.get('_links', []):
            self.actions[action['rel'] + '_action'] = self.create_action(action)

    def __getattr__(self, attr):
        # __getattr__ is only called when the attribute is not found by other means
        # attach the action methods to the instance
        try:
            return self.actions[attr]
        except KeyError:
            raise AttributeError


class Item(ApiObject):
    """
    Mapping class for an item object.
    """

    def __init__(self, base_url, data=None):
        data = data or {}
        self.title = data.get('title', '')
        self.body = data.get('body', '')
        self.created = data.get('created') or 0
        self.due = data.get('due') or 0
        self.state = data.get('state', 'open')
        self.task_id = data.get('task_id', None)

        self.base_url = base_url

        self.register_actions(data)

    def __str__(self):
        return json.dumps(self.json(), indent=2, separators=(',', ': '))

    def json(self):
        fields = ['task_id', 'title', 'body', 'created', 'due', 'state', 'base_url']
        ret = {}
        for field in fields:
            ret[field] = getattr(self, field)
        return ret


class ApiManager(ApiObject):
    """
    Mapping object for basic api object.
    """

    def __init__(self, base_url, data=None):
        data = data or {}

        self.base_url = base_url

        self.register_actions(data)


def create_items(data):
    """
    Function that creates an array of Item objects from a response json
    :param data: the json data received from the server
    :return: a list of Item objects
    """

    ret = []

    for item in data['data']['0']['tasks']:
        ret.append(Item(item))

    return ret

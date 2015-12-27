import datetime
from kivy.adapters.listadapter import ListAdapter

from kivy.app import App
from kivy.properties import DictProperty
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.popup import Popup

data = {
    "tasks": [
        {
            "status": "done",
            "title": "Buy groceries.",
            "body": "Milk, Coffee, Chocolate.",
            "created": 1450182780,
            "due": 1450187272
        },
        {
            "status": "open",
            "title": "Go to work.",
            "body": "Remember to bring suitcase.",
            "created": 1450191352,
            "due": 1450191412
        },
        {
            "status": "ongoing",
            "title": "Implement high-tech API",
            "body": "Plug-and-play cross-universe.",
            "created": 1450263412,
            "due": 1450429200
        },
    ]
}


class CListItemButton(ListItemButton):
    data = DictProperty()


class CPopup(Popup):
    data = DictProperty()


class CListView(ListView):

    @staticmethod
    def list_item_args_converter(row_index, record):
        return {
            'data': {
                'title': record['title'],
                'row': row_index,
                'status': record['status'],
                'body': record['body'],
                'created': datetime.datetime.fromtimestamp(record['created']),
                'due': datetime.datetime.fromtimestamp(record['due']),
                'root_list': record['root_list']
            }
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for item in data['tasks']:
            item['root_list'] = self

        self.data = data['tasks']
        self.adapter = ListAdapter(
            data=self.data,
            args_converter=self.list_item_args_converter,
            selection_mode='none',
            allow_empty_selection=True,
            cls=CListItemButton)


class MainApp(App):
    def build(self):
        super(MainApp, self).build()
        return self.root

if __name__ == '__main__':
    MainApp().run()

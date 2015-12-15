from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView

data = {
    "tasks": [
        {
            "status": "done",
            "title": "Buy groceries",
            "body": "Milk, Coffee, Chocolate.",
            "created": 1450182780,
            "due": 1450187272
        },
        {
            "status": "done",
            "title": "Go to work.",
            "body": "Remember to bring suitcase.",
            "created": 1450191352,
            "due": 1450191412
        },
        {
            "status": "done",
            "title": "Implement high-tech API",
            "body": "Plug-and-play cross-universe.",
            "created": 1450263412,
            "due": 1450429200
        },
    ]
}
class MainView(GridLayout):
    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(MainView, self).__init__(**kwargs)

        list_view = ListView(item_strings=[str(index) for index in range(100)])

        self.add_widget(list_view)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MainView(width=800))

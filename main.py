from kivy.app import App
from kivy.uix.gridlayout import GridLayout

import config
from views import TasksListView

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


class MainApp(App):
    def build(self):
        # required if kv file is used
        if config.use_kv_file:
            super(MainApp, self).build()

        self.root = GridLayout(
            cols=1,
            rows=1
        )

        self.root.add_widget(TasksListView(data=data['tasks']))

        return self.root

if __name__ == '__main__':
    MainApp().run()

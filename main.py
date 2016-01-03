from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import config
from views import TasksListView, AddEditPopup

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
    task_list = None
    add_button = None

    @staticmethod
    def on_add_new_task(instance):
        AddEditPopup(
            title='Add Task:',
            leave_callback=MainApp.on_add_popup_leave
        ).open()

    @staticmethod
    def on_add_popup_leave(popup):
        # save data
        print('saving data: %s', popup.result)

    def build(self):
        # required if kv file is used
        if config.use_kv_file:
            super(MainApp, self).build()

        self.root = GridLayout(
            cols=1
        )

        self.task_list = TasksListView(data=data['tasks'])
        self.add_button = Button(
            text='Add task..',
            height=30,
            background_color=(0.3, 1, 0.3, 1),
            size_hint_y=None
        )

        self.add_button.bind(on_press=self.on_add_new_task)

        self.root.add_widget(self.task_list)
        self.root.add_widget(self.add_button)

        return self.root

if __name__ == '__main__':
    MainApp().run()

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

import config
from api_manager import ApiManager, get_json
from views import TasksListView, AddEditPopup


class MainApp(App):
    task_list = None
    add_button = None

    @staticmethod
    def on_add_new_task(instance):
        aep = AddEditPopup(
            title='Add Task:',
            leave_callback=MainApp.on_add_popup_leave,
        )
        aep.context = instance.context
        aep.open()

    @staticmethod
    def on_add_popup_leave(popup):
        # save data
        if popup.accepted:
            popup.context['api_manager'].add_action(popup.result)
            popup.context['task_list'].update()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_manager = ApiManager(config.server_address,
                                      get_json(config.server_address + config.api_url_start)['data'][0])

    def build(self):
        # required if kv file is used
        if config.use_kv_file:
            super(MainApp, self).build()

        self.root = GridLayout(
            cols=1
        )

        self.task_list = TasksListView(api_manager=self.api_manager)

        self.add_button = Button(
            text='Add task..',
            height=30,
            background_color=(0.3, 1, 0.3, 1),
            size_hint_y=None
        )

        self.add_button.context = {
            'api_manager': self.api_manager,
            'task_list': self.task_list
        }

        self.add_button.bind(on_press=self.on_add_new_task)

        self.root.add_widget(self.task_list)
        self.root.add_widget(self.add_button)

        return self.root

if __name__ == '__main__':
    MainApp().run()

# todo: edit form and check all

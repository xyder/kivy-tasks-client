import datetime
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListView, ListItemButton

import config
from api_manager import Item
from views import AddEditPopup


def convert_time(timestamp):
    return str(datetime.datetime.fromtimestamp(int(timestamp)))


class CustomListItemButton(ListItemButton):

    def on_release(self):
        aep = AddEditPopup(
            item=self.item,
            title='Edit Task:',
            leave_callback=self.on_popup_leave
        )
        aep.parent_list = self.parent_list
        aep.open()

    @staticmethod
    def on_popup_leave(popup):
        if popup.accepted:
            popup.item.update_action(popup.result)
            popup.parent_list.update()

    @staticmethod
    def on_delete(instance):
        instance.item.delete_action()
        instance.parent_list.update()

    @staticmethod
    def create_label(**kwargs):
        ret = Label(
            text=kwargs.get('text', ''),
            font_size=kwargs.get('font_size', '15sp'),
            halign=kwargs.get('halign', 'left'),
            markup=kwargs.get('markup', True),
            color=kwargs.get('color', (1, 1, 1, 1))
        )

        ret.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))

        return ret

    def build_labels(self):
        ret = GridLayout(
            cols=3,
            rows=2,
            orientation='horizontal',
            x=10  # manual override for when 'pos' binding doesn't work
        )

        ret.title_label = CustomListItemButton.create_label(
            text='%s. [b]%s[/b]' % (self.row, self.item.title),
            font_size='20dp'
        )

        ret.status_label = CustomListItemButton.create_label(
            text='[b]%s[/b]' % self.item.state.upper(),
            color=(0.0, 0.5, 1.0, 1.0),
            halign='right',
        )

        ret.created_label = CustomListItemButton.create_label(
            text=convert_time(self.item.created),
        )

        ret.due_label = CustomListItemButton.create_label(
            text=convert_time(self.item.due),
            halign='right',
        )

        ret.delete_button = Button(
            markup=True,
            text='[b][color=220000]X[/color][/b]',
            background_color=(0, 0, 0, 0),
            size_hint_x=None,
            width=30
        )
        ret.delete_button.row = self.row
        ret.delete_button.item = self.item
        ret.delete_button.parent_list = self.parent_list
        ret.delete_button.bind(on_press=self.on_delete)

        ret.add_widget(ret.title_label)
        ret.add_widget(ret.status_label)
        ret.add_widget(ret.delete_button)
        ret.add_widget(ret.created_label)
        ret.add_widget(ret.due_label)

        return ret

    def __init__(self, **kwargs):
        self.item = kwargs.get('item', None)
        self.row = int(kwargs.get('row', -1)) + 1
        self.parent_list = kwargs.get('parent_list', None)
        self.deselected_color = (.7, .7, 1, 1)
        self.halign = 'center'
        self.markup = True
        self.height = 50
        self.size_hint_y = None

        super(CustomListItemButton, self).__init__(**kwargs)
        self.labels_container = self.build_labels()
        self.add_widget(self.labels_container)

        self.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))

        # note: 'pos' binding is not triggered on the last item in a list.
        self.bind(pos=lambda s, w: s.labels_container.setter('pos')(s, (w[0] + 10, w[1])))

        self.bind(size=lambda s, w: s.labels_container.setter('size')(s, (w[0] - 10, w[1])))


class TasksListView(ListView):
    data = None

    def list_item_args_converter(self, row_index, record):
        return {
            'item': Item(base_url=config.server_address, data=record),
            'row': row_index,
            'parent_list': self
        }

    def fetch_data(self):
        self.data = self.api_manager.list_action()['data'][0]['tasks']

    def update(self):
        self.fetch_data()
        self.adapter.data = self.data
        self.populate()

    def __init__(self, **kwargs):
        self.api_manager = kwargs.get('api_manager', None)
        self.fetch_data()

        super(TasksListView, self).__init__(**kwargs)
        self.adapter = ListAdapter(
            data=self.data,
            args_converter=self.list_item_args_converter,
            selection_mode='none',
            allow_empty_selection=True,
            cls=CustomListItemButton)

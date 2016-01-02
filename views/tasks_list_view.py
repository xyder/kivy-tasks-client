import datetime
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListView, ListItemButton
from views import AddEditPopup


class CustomListItemButton(ListItemButton):

    def on_release(self):
        AddEditPopup(
            data=self.data,
            title='Edit Task:',
            leave_callback=self.on_popup_leave
        ).open()

    @staticmethod
    def on_popup_leave(popup):
        if popup.accepted and popup.changed:
            # save data
            print('saving data: %s', popup.result)

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
            cols=2,
            rows=2,
            orientation='horizontal',
            x=10  # manual override for when 'pos' binding doesn't work
        )

        ret.title_label = CustomListItemButton.create_label(
            text='%s. [b]%s[/b]' % (self.data['row'], self.data['title']),
            font_size='20dp'
        )

        ret.status_label = CustomListItemButton.create_label(
            text='[b]%s[/b]' % self.data['status'].upper(),
            color=(0.0, 0.5, 1.0, 1.0),
            halign='right',
        )

        ret.created_label = CustomListItemButton.create_label(
            text=self.data['created'],
        )

        ret.due_label = CustomListItemButton.create_label(
            text=self.data['due'],
            halign='right',
        )

        ret.add_widget(ret.title_label)
        ret.add_widget(ret.status_label)
        ret.add_widget(ret.created_label)
        ret.add_widget(ret.due_label)

        return ret

    def __init__(self, **kwargs):
        self.data = kwargs.get('data', {})
        self.deselected_color = (.7, .7, 1, 1)
        self.halign = 'center'
        self.markup = True
        self.height = 50
        self.size_hint_y = None

        super().__init__(**kwargs)
        self.labels_container = self.build_labels()
        self.add_widget(self.labels_container)

        self.bind(width=lambda s, w: s.setter('text_size')(s, (w, None)))

        # note: 'pos' binding is not triggered on the last item in a list.
        self.bind(pos=lambda s, w: s.labels_container.setter('pos')(s, (w[0] + 10, w[1])))

        self.bind(size=lambda s, w: s.labels_container.setter('size')(s, (w[0] - 20, w[1])))


class TasksListView(ListView):
    @staticmethod
    def list_item_args_converter(row_index, record):
        return {
            'data': {
                'title': record['title'],
                'row': row_index + 1,
                'status': record['status'],
                'body': record['body'],
                'created': str(datetime.datetime.fromtimestamp(record['created'])),
                'due': str(datetime.datetime.fromtimestamp(record['due'])),
            },
        }

    def __init__(self, **kwargs):
        self.data = kwargs.get('data', [])

        super().__init__(**kwargs)
        self.adapter = ListAdapter(
            data=self.data,
            args_converter=self.list_item_args_converter,
            selection_mode='none',
            allow_empty_selection=True,
            cls=CustomListItemButton)

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
import config


class LabeledInput(GridLayout):
    def __init__(self, **kwargs):
        self.label_text = kwargs.get('label_text', '')
        self.input_text = kwargs.get('input_text', '')
        self.height = kwargs.get('height', 70)

        super(LabeledInput, self).__init__(
            cols=1,
            size_hint_y=None,
            **kwargs)

        self.label = Label(
            text=self.label_text,
            halign='left'
        )
        self.label.bind(size=self.label.setter('text_size'))

        self.input = TextInput(
            text=self.input_text,
            multiline=kwargs.get('multiline', False)
        )

        if 'input_height' in kwargs:
            self.input.size_hint_y = None
            self.input.height = kwargs['input_height']

        self.add_widget(self.label)
        self.add_widget(self.input)


class AddEditPopup(Popup):
    inputs = {}
    result = {}
    accepted = False

    @property
    def changed(self):
        return self.data != self.result

    def populate_result(self):
        for k in (x['key'] for x in config.form_input_formats):
            self.result[k] = self.inputs[k].input.text

    def on_dismiss(self):
        self.populate_result()
        self.leave_callback(self)

    @staticmethod
    def on_accept(instance):
        instance.parent_popup.accepted = True
        instance.parent_popup.dismiss()

    def build_buttons(self):
        ret = GridLayout(
            size_hint_y=None,
            height=30,
            rows=1,
            cols=2
        )

        ret.accept_button = Button(
            text='Save',
            background_color=(0.3, 1, 0.3, 1)
        )

        ret.cancel_button = Button(
            text='Cancel',
            background_color=(1.5, 0.3, 0.3, 1)
        )

        ret.accept_button.parent_popup = self
        ret.accept_button.bind(on_press=self.on_accept)
        ret.add_widget(ret.accept_button)

        ret.cancel_button.parent_popup = self
        ret.cancel_button.bind(on_press=self.dismiss)
        ret.add_widget(ret.cancel_button)

        return ret

    def build_inputs(self):
        ret = GridLayout(
            cols=1
        )

        for i in config.form_input_formats:
            formatter = i.get('formatter', None) or (lambda x: x)
            extra_args = i.get('args', {})

            labeled_input = LabeledInput(
                label_text=i['label'],
                input_text=formatter(self.data.get(i['key'], '')),
                **extra_args
            )

            self.inputs[i['key']] = labeled_input
            ret.add_widget(self.inputs[i['key']])

        return ret

    def __init__(self, **kwargs):
        super(AddEditPopup, self).__init__(**kwargs)

        self.content = kwargs.get('content', GridLayout(
            cols=1
        ))

        self.leave_callback = kwargs.get('leave_callback', lambda popup: None)

        self.data = kwargs.get('data', {})
        self.title = kwargs.get('title', 'Add/Edit task:')

        self.content.inputs_container = self.build_inputs()
        self.content.buttons_container = self.build_buttons()

        self.content.add_widget(self.content.inputs_container)
        self.content.add_widget(self.content.buttons_container)

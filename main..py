import arabic_reshaper
from bidi.algorithm import get_display
import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.text import LabelBase


LabelBase.register(
    name="Arabic",
    fn_regular="/storage/emulated/0/Download/Noto_Sans_Arabic (2)/static/NotoSansArabic-Regular.ttf"
)


def arabic(text):
    return get_display(
        arabic_reshaper.reshape(text)
    )


class ShopApp(App):

    def build(self):

        self.products = []

        self.file_path = os.path.join(
            self.user_data_dir,
            "products.json"
        )

        self.load_products()

        main = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        title = Label(
            text=arabic("متجري"),
            font_name="Arabic",
            font_size=42,
            bold=True,
            size_hint_y=None,
            height=70
        )

        main.add_widget(title)

        main.add_widget(Label(
            text=arabic("اسم المنتج"),
            font_name="Arabic",
            font_size=22,
            size_hint_y=None,
            height=35
        ))

        self.name_input = TextInput(
            multiline=False,
            font_name="Arabic",
            font_size=22,
            size_hint_y=None,
            height=55
        )

        main.add_widget(self.name_input)

        main.add_widget(Label(
            text=arabic("السعر"),
            font_name="Arabic",
            font_size=22,
            size_hint_y=None,
            height=35
        ))

        self.price_input = TextInput(
            multiline=False,
            input_filter="float",
            font_size=22,
            size_hint_y=None,
            height=55
        )

        main.add_widget(self.price_input)

        main.add_widget(Label(
            text=arabic("الكمية"),
            font_name="Arabic",
            font_size=22,
            size_hint_y=None,
            height=35
        ))

        self.quantity_input = TextInput(
            multiline=False,
            input_filter="int",
            font_size=22,
            size_hint_y=None,
            height=55
        )

        main.add_widget(self.quantity_input)

        buttons = BoxLayout(
            size_hint_y=None,
            height=60,
            spacing=10
        )

        add_button = Button(
            text=arabic("إضافة المنتج"),
            font_name="Arabic",
            font_size=21,
            bold=True
        )

        clear_button = Button(
            text=arabic("مسح الكل"),
            font_name="Arabic",
            font_size=21,
            bold=True
        )

        add_button.bind(
            on_press=self.add_product
        )

        clear_button.bind(
            on_press=self.clear_all
        )

        buttons.add_widget(add_button)
        buttons.add_widget(clear_button)

        main.add_widget(buttons)

        invoice_title = Label(
            text=arabic("الفاتورة"),
            font_name="Arabic",
            font_size=28,
            bold=True,
            size_hint_y=None,
            height=55
        )

        main.add_widget(invoice_title)

        self.list_box = BoxLayout(
            orientation="vertical",
            spacing=5
        )

        main.add_widget(self.list_box)

        self.count_label = Label(
            text=arabic("عدد المنتجات: 0"),
            font_name="Arabic",
            font_size=22,
            size_hint_y=None,
            height=40
        )

        self.total_label = Label(
            text=arabic("المجموع النهائي: 0"),
            font_name="Arabic",
            font_size=30,
            bold=True,
            size_hint_y=None,
            height=65
        )

        main.add_widget(self.count_label)
        main.add_widget(self.total_label)

        self.refresh_list()

        return main

    def add_product(self, instance):

        name = self.name_input.text

        if (
            not name
            or not self.price_input.text
            or not self.quantity_input.text
        ):
            return

        price = float(self.price_input.text)
        quantity = int(self.quantity_input.text)

        product = {
            "name": name,
            "price": price,
            "quantity": quantity
        }

        self.products.append(product)

        self.save_products()
        self.clear_inputs()
        self.refresh_list()

    def clear_inputs(self):

        self.name_input.text = ""
        self.price_input.text = ""
        self.quantity_input.text = ""

    def save_products(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.products,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load_products(self):

        if os.path.exists(self.file_path):

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.products = json.load(file)

    def refresh_list(self):

        self.list_box.clear_widgets()

        total = 0

        for index, product in enumerate(
            self.products
        ):

            product_total = (
                product["price"]
                * product["quantity"]
            )

            total += product_total

            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=55,
                spacing=5
            )

            text = Label(
                text=arabic(
                    product["name"]
                    + " - "
                    + str(product["price"])
                    + " × "
                    + str(product["quantity"])
                    + " = "
                    + str(product_total)
                ),
                font_name="Arabic",
                font_size=18
            )

            edit_button = Button(
                text=arabic("تعديل"),
                font_name="Arabic",
                font_size=17,
                size_hint_x=None,
                width=75
            )

            delete_button = Button(
                text=arabic("حذف"),
                font_name="Arabic",
                font_size=17,
                size_hint_x=None,
                width=65
            )

            edit_button.bind(
                on_press=lambda x, i=index:
                self.edit_product(i)
            )

            delete_button.bind(
                on_press=lambda x, i=index:
                self.delete_product(i)
            )

            row.add_widget(text)
            row.add_widget(edit_button)
            row.add_widget(delete_button)

            self.list_box.add_widget(row)

        self.count_label.text = (
            arabic("عدد المنتجات: ")
            + str(len(self.products))
        )

        self.total_label.text = (
            arabic("المجموع النهائي: ")
            + str(total)
        )

    def delete_product(self, index):

        del self.products[index]

        self.save_products()
        self.refresh_list()

    def edit_product(self, index):

        product = self.products[index]

        self.name_input.text = product["name"]
        self.price_input.text = str(
            product["price"]
        )
        self.quantity_input.text = str(
            product["quantity"]
        )

        del self.products[index]

        self.save_products()
        self.refresh_list()

    def clear_all(self, instance):

        self.products = []

        self.save_products()
        self.refresh_list()


ShopApp().run()
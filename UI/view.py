import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Tesi"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        self._page.bgcolor = "#121212"
        self._page.window_height = 800
        self._page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#d90429",
                secondary="#d90429",
                surface="#1e1e1e",
                background="#121212",
                on_primary="white",
                on_surface="white",
                on_background="white",
                on_secondary="white"
            )
        )
        page.window_center()
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddAnno = None
        self._btnCreaGrafo = None
        self._btnCercaCamminoMin = None
        self._txtK = None
        self._ddCircuitoVincolante = None
        self._txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Ottimizzazione del trasporto attrezzature nel calendario di F1", color="#d90429", font_family="Roboto Mono", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

        # row1
        self._ddAnno = ft.Dropdown(label="Anno", dense=True, border_color="#d90429", bgcolor="#1e1e1e", color="white", label_style=ft.TextStyle(color="white"), width=100)
        self._controller.fillDDYear()
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo", icon=ft.icons.CREATE_OUTLINED, bgcolor="#d90429", color="white", on_click=self._controller.handleCreaGrafo)

        cont = ft.Container(self._ddAnno, width=250, alignment=ft.alignment.center)
        row1 = ft.Row([self._ddAnno, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)

        # row2
        self._ddCircuitoVincolante = ft.Dropdown(label="Circuito da visitare", dense=True, border_color="#d90429", bgcolor="#1e1e1e", color="white", label_style=ft.TextStyle(color="white"), width=280)
        self._txtK = ft.TextField(label="Entro quante gare", dense=True, border_color="#d90429", bgcolor="#1e1e1e", color="white", label_style=ft.TextStyle(color="white"),  width=200)

        row2 = ft.Row([self._ddCircuitoVincolante, self._txtK], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        # row3
        self._btnCercaCamminoMin = ft.ElevatedButton(text="Cerca cammino minimo", icon=ft.icons.TRAVEL_EXPLORE_OUTLINED, bgcolor="#d90429", color="white", on_click=self._controller.handleCercaCamminoMin)
        row3 = ft.Row([ft.Container(self._btnCercaCamminoMin, width=240)], alignment=ft.MainAxisAlignment.CENTER)

        # aggiungo tutto
        self._page.controls.append(ft.Container(height=3))
        self._page.controls.append(self._title)
        self._page.controls.append(ft.Container(height=3))
        self._page.controls.append(row1)
        self._page.controls.append(ft.Container(height=3))
        self._page.controls.append(row2)
        self._page.controls.append(ft.Container(height=3))
        self._page.controls.append(row3)

        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()


    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()









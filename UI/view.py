import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Tesi"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 800
        page.window_center()
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddAnno = None
        self._txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Studio delle distanze tra circuiti nel calendario F1 per l’ottimizzazione del trasporto attrezzature", color="blue", size=16)
        self._page.controls.append(self._title)


        self._ddAnno = ft.Dropdown(label="Anno")
        self._controller.fillDDYear()
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo", on_click=self._controller.handleCreaGrafo)

        cont = ft.Container(self._ddAnno, width=250, alignment=ft.alignment.top_left)
        row1 = ft.Row([cont, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.END)

        self._ddCircuitoVincolante = ft.Dropdown(label="Circuito da vincolare", width=350)
        self._txtK = ft.TextField(label="Entro quante gare", width=200)
        row2 = ft.Row([self._ddCircuitoVincolante, self._txtK], alignment=ft.MainAxisAlignment.CENTER)

        self._btnCercaCamminoMin = ft.ElevatedButton(text="Cerca cammino minimo", on_click=self._controller.handleCercaCamminoMin)
        row3 = ft.Row([ft.Container(self._btnCercaCamminoMin, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
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

    def update_page(self):
        self._page.update()









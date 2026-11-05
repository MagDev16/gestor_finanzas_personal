import FreeSimpleGUI as sg

sg.theme("Topanga")

# 1. Diseño del layout completo (con la tabla y el botón Agregar incluidos)
layout = [
    [
        sg.Text(
            "Gestor de Finanzas Personales",
            font=("Roboto", 16, "bold"),
            pad=(0, 10),
        )
    ],
    [sg.HorizontalSeparator()],
    # Sección de registro
    [
        sg.Frame(
            "Registrar Movimiento",
            [
                [
                    sg.Text("Tipo:", size=(10, 1)),
                    sg.Combo(
                        ["Ingreso", "Gasto"],
                        default_value="Gasto",
                        key="-TIPO-",
                        readonly=True,
                        size=(15, 1),
                    ),
                ],
                [
                    sg.Text("Categoria:", size=(10, 1)),
                    sg.InputText(
                        key="-CATEGORIA-",
                        size=(15, 1),
                        tooltip="Ej: Comida, Salario, Transporte",
                    ),
                ],
                [
                    sg.Text("Monto($):", size=(10, 1)),
                    sg.InputText(
                        key="-MONTO-",
                        size=(17, 1),
                    ),
                ],
                [
                    sg.Text("Descripción:", size=(10, 1)),
                    sg.InputText(
                        key="-DESCRIPCION-",
                        size=(17, 1),
                    ),
                ],
                [
                    sg.Button(
                        "Agregar",
                        key="-BTN_AGREGAR-",
                        button_color=("white", "green"),
                        size=(12, 1),
                    ),
                    sg.Button(
                        "Limpiar",
                        key="-BTN_LIMPIAR-",
                        button_color=("white", "gray"),
                        size=(12, 1),
                    ),
                ],
            ],
        )
    ],
    # Sección de Historial y Balance
    [
        sg.Text(
            "Historial de Transacciones",
            font=("Helvetica", 12, "bold"),
            pad=(0, 5),
        )
    ],
    [
        sg.Table(
            values=[],
            headings=["Tipo", "Categoría", "Monto ($)", "Descripción"],
            auto_size_columns=False,
            col_widths=[12, 15, 12, 25],
            justification="center",
            key="-TABLA-",
            row_height=25,
        )
    ],
    [
        sg.Text(
            "Balance Total: $0.00",
            font=("Helvetica", 12, "bold"),
            key="-BALANCE-",
            text_color="lightgreen",
        )
    ],
    [sg.Button("Salir", button_color=("white", "firebrick3"), size=(10, 1))],
]

# Crear la ventana
window = sg.Window(
    "Gestor de Finanzas Personales",
    layout,
    finalize=True,
    resizable=True,
)

# Inicializar variables de estado
transacciones = []
balance_total = 0.0

# Bucle de eventos
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Salir":
        break

    if event == "-BTN_LIMPIAR-":
        window["-TIPO-"].update("Gasto")
        window["-CATEGORIA-"].update("")
        window["-MONTO-"].update("")
        window["-DESCRIPCION-"].update("")

    # Lógica del botón Agregar (el fragmento que compartiste)
    if event == "-BTN_AGREGAR-":
        tipo = values["-TIPO-"]
        categoria = values["-CATEGORIA-"]
        monto_str = values["-MONTO-"]
        descripcion = values["-DESCRIPCION-"]

        # Validar campos vacíos
        if not categoria or not monto_str:
            sg.popup_error(
                "Por favor completa al menos la categoría y el monto.",
                title="Error de validación",
            )
            continue

        # Validar que el monto sea un número válido
        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            sg.popup_error(
                "El monto debe ser un número válido mayor a 0.", title="Error"
            )
            continue

        # Calcular balance total
        if tipo == "Ingreso":
            balance_total += monto
        else:
            balance_total -= monto

        # Agregar a la lista de transacciones
        transacciones.append([tipo, categoria, f"${monto:.2f}", descripcion])

        # Actualizar la tabla y el balance en la interfaz
        window["-TABLA-"].update(values=transacciones)
        color_balance = "lightgreen" if balance_total >= 0 else "salmon"
        window["-BALANCE-"].update(
            f"Balance Total: ${balance_total:.2f}", text_color=color_balance
        )

        # Limpiar entradas de texto tras agregar con éxito
        window["-CATEGORIA-"].update("")
        window["-MONTO-"].update("")
        window["-DESCRIPCION-"].update("")

window.close()
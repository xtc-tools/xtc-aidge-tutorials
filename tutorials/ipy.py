from types import SimpleNamespace as NS

config = NS()


def display_radio(name: str, desc: str):
    import ipywidgets as widgets
    from IPython.display import display

    radio = widgets.RadioButtons(
        options=[("True", True), ("False", False)],
        description=desc,
    )
    setattr(config, name, radio)
    display(radio)


def display_checkbox(name: str, *args: str):
    import ipywidgets as widgets
    from IPython.display import display

    ops = {arg: widgets.Checkbox(value=False, description=arg) for arg in args}
    setattr(config, name, NS(**ops))
    display(*ops.values())


def display_nradio(name: str, desc: str, *args: str):
    import ipywidgets as widgets
    from IPython.display import display

    options = [(arg, arg) for arg in args]
    radio = widgets.RadioButtons(
        options=options,
        description=desc,
    )
    setattr(config, name, radio)
    display(radio)


def nradio_value(name: str, field: str):
    value = getattr(config, name).value
    return value == field

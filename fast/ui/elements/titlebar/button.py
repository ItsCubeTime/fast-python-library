from nicegui import ui
# from ... import serveFiles


class button:
    "Top right buttons for the window titlebar."

    def __init__(self, cb, iconName="check", transparentBackground = False) -> None:
        with ui.column() as column:
            if transparentBackground:
                column.style(replace='background-color:transparent;')
            column._classes.clear()
            column.style(f"border-radius: 5px; {'border-color: transparent; background-color: transparent;' if transparentBackground else 'border-color: rgba(0, 0, 0, 0.08); backdrop-filter: blur(5px); background-color: rgba(0, 0, 0, 0.08);'} height:25px; width: 25px; justify-content: center; align-items: center; display:flex; border-width: 2px;  cursor: pointer;")
            # ui.image(serveFiles.serveFile)
            ui.icon(iconName)
            column.on("click", cb)

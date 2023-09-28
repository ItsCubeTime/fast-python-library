from __future__ import annotations

import nicegui
from nicegui import ui

class Colors:
    """instanciate before use"""

    darkMode = True
    "Do not set directly"

    fierceRed = "#C53A47"
    red = "#C64845"
    tigerEye = "#C65644"
    leopard = "#C66344"
    transparent = "#1a1c1e00"

    accentColorStrong = fierceRed
    accentColorNeutral = red
    accentColorWeak = tigerEye
    accentColorWeaker = leopard

    shadowDark = "#1A1C1E"
    shadow = "#252526"

    angelWhite = "#fafafa"
    linenWhite = "#ececec"
    featherWhite = "#adadad"

    onlineGreen = "#23A55A"

    neutral_DarkModeOff = angelWhite
    neutral_DarkModeOn = shadow

    @property
    def neutral(self):
        return self.neutral_DarkModeOn if self.darkMode else self.neutral_DarkModeOff
    
    @property
    def pageBackground(self):
        "The color used for the background of the entire page. This color would also be used as the OS-level window background if its not transparent."
        return self.neutral

    @property
    def neutral_Opposite(self):
        return self.neutral_DarkModeOn if not self.darkMode else self.neutral_DarkModeOff

    neutralDark_DarkModeOff = featherWhite
    neutralDark_DarkModeOn = shadowDark

    @property
    def neutralDark(self):
        return self.neutralDark_DarkModeOn if self.darkMode else self.neutralDark_DarkModeOff

    @property
    def neutralDark_Opposite(self):
        return self.neutralDark_DarkModeOn if not self.darkMode else self.neutralDark_DarkModeOff
    



    clients: dict[int, ] = dict()
    def setDarkMode(self: Colors, value: bool, client: nicegui.Client = nicegui.globals.get_client()):
        self.darkMode=value
        varCssString = ''
        for varName in dir(self):
            var = getattr(self, varName)
            isColor = isinstance(var, str) and varName[:2] != '__'
            if isColor:
                # We assume that this is a color attribute.
                varCssString += f'--{varName}:{var};'
            # else:
            varCssString += 'color: var(--neutral_Opposite);'
            # print(f"varT: {type(var)} name: {varName} isColor: {isColor}")
        varCssStringWrapped = f'''
        <style class="fastCssColorVariables">:root {{ {varCssString} }} </style>
        '''
        from ... import asyncronous
        try:
            asyncronous.runAsync( 
                client.run_javascript(f'''
function add_FastCssColorVariables_StyleElement() {{
let fastCssColorVariables_Elements = document.getElementsByClassName(`fastCssColorVariables`);

// @note Reomve old style elements
let i = -1;
while (i < fastCssColorVariables_Elements.length-1) {{
    i += 1;
    let fastCssColorVariables_Element = fastCssColorVariables_Elements[0];
    // console.log(`awesome: ${{fastCssColorVariables_Element}}`);
    fastCssColorVariables_Element.remove();
}}

// @note Create new html style element
const fastCssColorVariables_Element_New = document.createElement("style");
fastCssColorVariables_Element_New.classList.add("fastCssColorVariables");
fastCssColorVariables_Element_New.innerHTML = `{varCssStringWrapped}`;
document.head.appendChild(fastCssColorVariables_Element_New);  

}}
add_FastCssColorVariables_StyleElement();                           
''', respond=False)
            )                                                                                                                                                                                    
        except Exception as exc:
            print(f" setDarkMode: {exc}")
        client.content.default_slot.parent.style(add=varCssString)

        # ui.add_body_html(varCssString)
        # ui.element('div')
        # print(f"css -> {varCssString} <-")
        ui.colors(primary=self.accentColorNeutral, secondary=self.accentColorWeak,accent=self.accentColorStrong,dark=self.neutralDark, positive=self.onlineGreen,negative=self.red,warning=self.leopard) # @todo set a color for "info" param
        # ui.dark_mode(value)
        
        # return
        ui.notify(f"Dark mode {'enabled' if self.darkMode else 'disabled'}!")

    def toggleDarkMode(self, client: nicegui.Client=nicegui.globals.get_client()):
        self.setDarkMode(not self.darkMode, client)



colors = Colors()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from calculations.Beam import Beam

class MenuUI(Screen):
    pass

class BeamUI(Screen):
    def on_submit(self):
        self.parameters = {
            '_fc': self.ids.fc_input.text,
            '_fy': self.ids.fy_input.text,
            '_es': self.ids.Es_input.text,
            'width': self.ids.width_input.text,
            'height': self.ids.height_input.text,
            'steeldim' : self.ids.sdim_input.text,
            'cover' : self.ids.cover_input.text,
            'ultimateMoment': self.ids.ultmoment_input.text,
            'rebarSize' : self.ids.rebar_input.text
        }
        new_parameters = {}
        for key, value in self.parameters.items():
            if value != '':
                try:
                    new_parameters[key] = int(value)
                except ValueError:
                    new_parameters[key] = float(value)
            else:
                pass
        beam_instance = Beam(**new_parameters)
        width = beam_instance.width
        height = beam_instance.height
        cover = beam_instance.cover
        sdim = beam_instance.steeldim
        rebarSize = beam_instance.rebarSize
        ultmoment = beam_instance.ultimateMoment
        fc = beam_instance._fc
        fy = beam_instance._fy
        Es = beam_instance._es
        self.ids.height_input.text = str(height)
        self.ids.width_input.text = str(width)
        self.ids.cover_input.text = str(cover)
        self.ids.sdim_input.text = str(sdim)
        self.ids.rebar_input.text = str(rebarSize)
        self.ids.ultmoment_input.text = str(ultmoment)
        self.ids.fc_input.text = str(fc)
        self.ids.fy_input.text = str(fy)
        self.ids.Es_input.text = str(Es)
        print('Sucessfully calculated')

class DetailUI(Screen):
    pass

class ColumnUI(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuUI(name='Menu_UI'))
        sm.add_widget(BeamUI(name='Beam_UI'))
        sm.add_widget(ColumnUI(name='Column_UI'))
        sm.add_widget(DetailUI(name='Detail_UI'))
        return sm

if __name__ == '__main__':
    MyApp().run()

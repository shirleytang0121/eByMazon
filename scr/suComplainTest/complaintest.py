from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen



class suComplainPage(Screen):
    def displayComplain(self):
        complains=[{'userID':'userID1','itemID':'itemID1','complain':'shipping too slow','time':'3:00'},
                   {'userID':'userID2','itemID':'itemID2','complain':'too expensive','time':'3:00'}]

        self.ids['complains'].data = complains
    
    def back(self):
        pass
    
    def approveComplain(self):
        pass
    
    def rejectComplain(self):
        pass


class MyApp(App):
    def build(self):
        return Builder.load_file('suComplain.kv')

if __name__ == '__main__':
    MyApp().run()
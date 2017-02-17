'''Screen Schedule
'''

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.factory import Factory

app = App.get_running_app()


class ScreenSchedule(Screen):
    '''
    Screen to display the schedule as per schedule.json generated by
    pydelhiconf.network every time the app is started. A default
    schedule is provided.

    Screen looks like:

    -----------------------------------------
    | YYYY-MM-DD                            | <- Date of event
    |                                       |
    |           HH:MM-HH:MM                 | <- Start time - End time
    |                                       |
    |           Title                       | <- Title of talk/workshop
    |           Type                        | <- Type: Talk/Workshop
    |           Speaker                     | <- Name of speaker
    |           .                           |
    |           .                           |
    -----------------------------------------

    '''

    Builder.load_string('''
<Topic@Label>
    canvas.before:
        Color
            rgba: app.base_inactive_light
        Rectangle
            size: dp(300), self.height
            pos: self.right - dp(300), self.y
        Color
            rgba: app.base_inactive_light[:3]+[.5]
        Rectangle
            size: dp(300), self.height
            pos: self.right - dp(310), self.y - dp(10)
    font_size: dp(27)
    text_size: self.width - dp(10), self.height
    size_hint_y: None
    height: dp(50)
    halign: 'right'
    valign: 'middle'

<AccordionItemTitle>
    text_size: self.width - dp(10), self.height
    halign: 'left'
    valign: 'middle'

<AccordionItem>
    back_color: app.base_active_color
    canvas.before:
        Color
            rgba: root.back_color or (1, 1, 1, 1)
        Rectangle
            size: dp(270), dp(36)
            pos: self.x, self.top - dp(36)
        Color
            rgba: (list(root.back_color[:3])+[.3]) if root.back_color else (1, 1, 1, 1)
        Rectangle
            size: dp(270), dp(36)
            pos: self.x + dp(7), self.top - (dp(36) + dp(7)) 

<TimeSlice@Label>
    text: app.start_time + '-' + app.end_time
    size_hint_y: None
    height: dp(27)
    background_color: app.base_active_color[:3] + [.3]
    canvas.before:
        Color
            rgba: root.background_color if root.background_color else (1, 1, 1, 1)
        Rectangle
            size: self.size
            pos: self.pos
   
<ScreenSchedule>
    name: 'ScreenSchedule'
    BoxLayout
        spacing: dp(20)
        orientation: 'vertical'
        padding: dp(4)
        Topic
            text: app.event_name
        Accordion
            id: accordian_days
            orientation: 'vertical'
 ''')


    def on_enter(self):
        '''Series of actions to be performed when Schedule screen is entered
        '''
        
        self.ids.accordian_days.clear_widgets()
        from network import get_data

        # this should update the file on disk
        event = get_data('event')
        schedule = get_data('schedule')

        # read the file from disk
        app.event_name = event['name']
        app.venue_name = event['venue']
        start_date = event['start_date']
        end_date = event['end_date']
        
        dates = schedule['results'][0].keys()     

        for date in dates:
            cday = Factory.AccordionItem(title=date)
            self.ids.accordian_days.add_widget(cday)
            sched = schedule['results'][0][date]          
            items = len(sched)
            sv = ScrollView()
            gl = GridLayout(cols=1,
                            size_hint_y=None,
                            padding='2dp',
                            spacing='2dp')
            i = 0
            for i in xrange(0, items):
                app.start_time = sched[i]['start_time']
                app.end_time = sched[i]['end_time']
                ts = Factory.TimeSlice()
                gl.add_widget(ts)
                gl.add_widget(Label(text=sched[i]['title'], height='27dp',
                    size_hint_y=None))
                gl.add_widget(Label(text='Type: ' + sched[i]['type'],
                    height='27dp', size_hint_y=None))
                gl.add_widget(Label(text='Speaker: ' + sched[i]['speaker_name'],
                    height='27dp', size_hint_y=None))
                
                i+=1

            sv.add_widget(gl)
            cday.add_widget(sv)
            

            # TODO: Dates are not sorted

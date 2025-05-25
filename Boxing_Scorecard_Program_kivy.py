from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window

class BoxingApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # Colors for text inputs
        self.red_color = (1, 0, 0, 1)  # red
        self.blue_color = (0, 0, 1, 1)  # blue

        # Input grid for fighters and rounds
        self.input_grid = GridLayout(
            cols=2, row_force_default=True, row_default_height=dp(40), spacing=dp(10), size_hint_y=None
        )
        self.input_grid.bind(minimum_height=self.input_grid.setter('height'))

        # Red Corner label and input
        red_label = Label(
            text="[b]Red Corner:[/b]", markup=True,
            size_hint_x=None, width=dp(100),
            halign="left", valign="middle",
            font_size='16sp',
            text_size=(dp(100), None)
        )
        red_label.bind(texture_size=red_label.setter('size'))
        self.input_grid.add_widget(red_label)

        self.fighter1_input = TextInput(
            multiline=False, foreground_color=self.red_color, size_hint_x=0.7
        )
        self.input_grid.add_widget(self.fighter1_input)

        # Blue Corner label and input
        blue_label = Label(
            text="[b]Blue Corner:[/b]", markup=True,
            size_hint_x=None, width=dp(100),
            halign="left", valign="middle",
            font_size='16sp',
            text_size=(dp(100), None)
        )
        blue_label.bind(texture_size=blue_label.setter('size'))
        self.input_grid.add_widget(blue_label)

        self.fighter2_input = TextInput(
            multiline=False, foreground_color=self.blue_color, size_hint_x=0.7
        )
        self.input_grid.add_widget(self.fighter2_input)

        # Rounds label and input
        rounds_label = Label(
            text="[b]Rounds:[/b]", markup=True,
            size_hint_x=None, width=dp(100),
            halign="left", valign="middle",
            font_size='16sp',
            text_size=(dp(100), None)
        )
        rounds_label.bind(texture_size=rounds_label.setter('size'))
        self.input_grid.add_widget(rounds_label)

        self.rounds_input = TextInput(
            multiline=False, input_filter='int', size_hint_x=0.7
        )
        self.input_grid.add_widget(self.rounds_input)

        self.add_widget(self.input_grid)

        # Start button
        self.start_button = Button(text="Start Fight", size_hint_y=None, height=dp(40))
        self.start_button.bind(on_press=self.start_fight)
        self.add_widget(self.start_button)

        # Message label for errors or info
        self.message_label = Label(text="", size_hint_y=None, height=dp(30))
        self.add_widget(self.message_label)

        # Fight state variables
        self.fighter1 = ""
        self.fighter2 = ""
        self.num_rounds = 0
        self.current_round = 1
        self.fighter1_total = 0
        self.fighter2_total = 0

    def start_fight(self, instance):
        self.fighter1 = self.fighter1_input.text.strip().title()
        self.fighter2 = self.fighter2_input.text.strip().title()

        try:
            self.num_rounds = int(self.rounds_input.text)
            if self.num_rounds <= 0:
                self.message_label.text = "Number of rounds must be positive."
                return
        except ValueError:
            self.message_label.text = "Enter a valid number of rounds."
            return

        if not self.fighter1 or not self.fighter2:
            self.message_label.text = "Please enter both fighter names."
            return

        # Clear UI and start round scoring
        self.clear_widgets()
        self.show_round_input()

    def show_round_input(self):
        self.clear_widgets()
        self.padding = dp(10)
        self.spacing = dp(10)

        round_label = Label(
            text=f"Round {self.current_round} of {self.num_rounds}",
            font_size='18sp',
            size_hint_y=None,
            height=dp(40),
        )
        self.add_widget(round_label)

        # Grid for scores
        scores_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        scores_grid.bind(minimum_height=scores_grid.setter('height'))

        # Red Corner score input
        red_label = Label(
            text=f"[b]{self.fighter1} (Red Corner) score (0-10):[/b]", markup=True,
            size_hint_x=None, width=dp(150),
            halign="left", valign="middle",
            font_size='16sp',
            text_size=(dp(150), None),
            size_hint_y=None, height=dp(40)
        )
        red_label.bind(texture_size=red_label.setter('size'))
        scores_grid.add_widget(red_label)

        self.f1_score_input = TextInput(
            multiline=False, input_filter='int', size_hint_x=0.7, size_hint_y=None, height=dp(40)
        )
        scores_grid.add_widget(self.f1_score_input)

        # Blue Corner score input
        blue_label = Label(
            text=f"[b]{self.fighter2} (Blue Corner) score (0-10):[/b]", markup=True,
            size_hint_x=None, width=dp(150),
            halign="left", valign="middle",
            font_size='16sp',
            text_size=(dp(150), None),
            size_hint_y=None, height=dp(40)
        )
        blue_label.bind(texture_size=blue_label.setter('size'))
        scores_grid.add_widget(blue_label)

        self.f2_score_input = TextInput(
            multiline=False, input_filter='int', size_hint_x=0.7, size_hint_y=None, height=dp(40)
        )
        scores_grid.add_widget(self.f2_score_input)

        self.add_widget(scores_grid)

        # Buttons layout
        btn_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))

        self.ko_button = Button(text="Knockout?")
        self.ko_button.bind(on_press=self.ask_knockout)
        btn_layout.add_widget(self.ko_button)

        self.submit_button = Button(text="Submit Scores")
        self.submit_button.bind(on_press=self.submit_scores)
        btn_layout.add_widget(self.submit_button)

        self.add_widget(btn_layout)

        # Message label for errors/info
        self.message_label = Label(text="", size_hint_y=None, height=dp(30))
        self.add_widget(self.message_label)

    def submit_scores(self, instance):
        try:
            f1_score = int(self.f1_score_input.text)
            f2_score = int(self.f2_score_input.text)
            if not (0 <= f1_score <= 10 and 0 <= f2_score <= 10):
                raise ValueError
        except ValueError:
            self.message_label.text = "Scores must be integers from 0 to 10."
            return

        self.fighter1_total += f1_score
        self.fighter2_total += f2_score

        if self.current_round < self.num_rounds:
            self.current_round += 1
            self.show_round_input()
        else:
            self.show_results()

    def ask_knockout(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        label = Label(
            text=f"Who won by KO? Enter '{self.fighter1}' or '{self.fighter2}':",
            size_hint_y=None, height=dp(40),
        )
        content.add_widget(label)

        self.ko_winner_input = TextInput(multiline=False, size_hint_y=None, height=dp(40))
        content.add_widget(self.ko_winner_input)

        btn_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        ok_btn = Button(text="OK")
        cancel_btn = Button(text="Cancel")
        btn_layout.add_widget(ok_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)

        self.ko_popup = Popup(title="Knockout Winner", content=content, size_hint=(0.75, 0.5))

        ok_btn.bind(on_press=self.handle_ko_winner)
        cancel_btn.bind(on_press=lambda _: self.ko_popup.dismiss())

        self.ko_popup.open()

    def handle_ko_winner(self, instance):
        winner = self.ko_winner_input.text.strip().title()
        if winner == self.fighter1 or winner == self.fighter2:
            self.ko_popup.dismiss()
            self.clear_widgets()
            self.add_widget(Label(
                text=f"Knockout! {winner} wins by KO in Round {self.current_round}!\nFight Over!",
                font_size='20sp',
                halign='center'
            ))
        else:
            self.message_label.text = "Invalid fighter name for KO."

    def show_results(self):
        self.clear_widgets()
        self.padding = dp(10)
        self.spacing = dp(10)

        self.add_widget(Label(text="=== Final Score ===", font_size='20sp', size_hint_y=None, height=dp(40)))
        self.add_widget(Label(text=f"{self.fighter1} (Red Corner): {self.fighter1_total}", font_size='18sp'))
        self.add_widget(Label(text=f"{self.fighter2} (Blue Corner): {self.fighter2_total}", font_size='18sp'))

        if self.fighter1_total > self.fighter2_total:
            winner = self.fighter1
            winner_corner = "Red Corner"
        elif self.fighter2_total > self.fighter1_total:
            winner = self.fighter2
            winner_corner = "Blue Corner"
        else:
            winner = None

        if winner:
            self.add_widget(Label(text=f"\nWinner: {winner} ({winner_corner})", font_size='20sp'))
        else:
            self.add_widget(Label(text="\nResult: It's a draw!", font_size='20sp'))

        self.add_widget(Label(text="--- Fight Completed! ---", font_size='16sp'))

class BoxingAppMain(App):
    def build(self):
        # Optional: set window size for desktop testing
        Window.size = (400, 600)
        return BoxingApp()

if __name__ == "__main__":
    BoxingAppMain().run()


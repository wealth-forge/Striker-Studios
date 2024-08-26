from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.clock import Clock
import random

# Force the app to start in landscape mode
Window.rotation = 270

# Questions and answers (editable list of dictionaries)
questions = [
    {"question": "Which planet is known as the Red Planet?", "answers": ["Mars", "Jupiter", "Earth", "Venus"]},
    {"question": "Who wrote 'Romeo and Juliet'?", "answers": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"]},
    {"question": "What is the capital of France?", "answers": ["Paris", "Berlin", "Rome", "Madrid"]},
    {"question": "What is the largest mammal?", "answers": ["Blue Whale", "Elephant", "Giraffe", "Shark"]},
    {"question": "Which element has the chemical symbol 'O'?", "answers": ["Oxygen", "Gold", "Iron", "Helium"]},
    {"question": "How many continents are there?", "answers": ["Seven", "Five", "Six", "Eight"]},
    {"question": "What is the hardest natural substance on Earth?", "answers": ["Diamond", "Gold", "Iron", "Quartz"]},
    {"question": "Who painted the Mona Lisa?", "answers": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Claude Monet"]},
    {"question": "Which country is home to the kangaroo?", "answers": ["Australia", "Canada", "China", "Brazil"]},
    {"question": "What is the tallest mountain in the world?", "answers": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"]}
]

# Prize money for each correct answer
prizes = [100, 200, 500, 1000, 2000, 5000, 10000, 50000, 100000, 1000000]

# Shuffle the questions to make the game more interesting
random.shuffle(questions)

class MillionaireApp(App):
    def build(self):
        self.current_question = 0
        self.correct_answer = ""
        self.touch_sound = SoundLoader.load('touch.mp3')

        # Main Layout: Horizontal Box Layout
        self.layout = BoxLayout(orientation="horizontal", padding=20, spacing=10)

        # Show the start screen with the Play button
        self.show_start_screen()

        return self.layout

    def show_start_screen(self):
        # Clear the current layout
        self.layout.clear_widgets()

        # Create the Play Button
        play_button = Button(text="Play", font_size=32, size_hint=(0.3, 0.2), background_color=(0, 0.5, 1, 1))
        play_button.bind(on_press=self.start_game)

        # Add the Play Button to the layout
        self.layout.add_widget(play_button)

    def start_game(self, instance):
        # Clear the layout and start the game
        self.layout.clear_widgets()
        self.build_game_layout()
        self.next_question()

    def build_game_layout(self):
        # Prize List Section (left side)
        self.prize_list = BoxLayout(orientation='vertical', size_hint=(0.2, 1), padding=10, spacing=10)
        self.update_prize_list()
        self.layout.add_widget(self.prize_list)

        # Question Section (middle section)
        self.question_section = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint=(0.6, 1))
        with self.question_section.canvas.before:
            Color(0.2, 0.2, 0.5, 1)  # Dark blue background
            self.rect = RoundedRectangle(size=self.question_section.size, pos=self.question_section.pos, radius=[20])
            self.question_section.bind(size=self._update_rect, pos=self._update_rect)

        self.question_label = Label(text="", font_size=28, halign="center", valign="middle", color=(1, 1, 1, 1), bold=True)
        self.question_section.add_widget(self.question_label)
        self.layout.add_widget(self.question_section)

        # Answers Section (right side)
        self.answers_section = GridLayout(cols=2, padding=10, spacing=10, size_hint=(0.4, 1))
        self.buttons = []
        for i in range(4):
            btn = Button(text="", font_size=20, size_hint=(1, 0.5), background_color=(0.1, 0.6, 0.1, 1), color=(1, 1, 1, 1))
            btn.bind(on_press=self.check_answer)
            self.answers_section.add_widget(btn)
            self.buttons.append(btn)
        
        self.layout.add_widget(self.answers_section)
        
        self.next_question()
        return self.layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_prize_list(self):
        self.prize_list.clear_widgets()
        for i, prize in enumerate(prizes):
            prize_label = Label(text=f"${prize}", font_size=20, halign="center", valign="middle", color=(1, 1, 1, 1))
            if i == self.current_question:  # Highlight the current prize
                prize_label.color = (1, 1, 0, 1)  # Highlight in yellow
            self.prize_list.add_widget(prize_label)

    def next_question(self):
        if self.current_question < len(questions):
            question_data = questions[self.current_question]
            self.correct_answer = question_data["answers"][0]
            shuffled_answers = question_data["answers"].copy()
            random.shuffle(shuffled_answers)

            self.question_label.text = f"Question {self.current_question + 1} for ${prizes[self.current_question]}:\n\n{question_data['question']}"
            
            for i, btn in enumerate(self.buttons):
                btn.text = shuffled_answers[i]
                btn.background_color = (0.1, 0.6, 0.1, 1)  # Reset background color to default
            
            self.update_prize_list()  # Update prize list highlight
        else:
            self.end_game("Congratulations! You've won $1,000,000!")

    def check_answer(self, instance):
        if self.touch_sound:
            self.touch_sound.play()

        correct = instance.text == self.correct_answer
        if correct:
            instance.background_color = (0, 1, 0, 1)  # Green color for correct answer
        else:
            instance.background_color = (1, 0, 0, 1)  # Red color for wrong answer

        # Highlight answer color for 3 seconds
        Clock.schedule_once(lambda dt: self.reset_buttons(correct), 1)

    def reset_buttons(self, correct):
        # Reset button colors and add delay before moving to next question or showing popup
        for btn in self.buttons:
            if btn.background_color == (0, 1, 0, 1) or btn.background_color == (1, 0, 0, 1):
                btn.background_color = (0.1, 0.6, 0.1, 1)  # Reset color
        Clock.schedule_once(lambda dt: self.handle_question_result(correct), 0)

    def handle_question_result(self, correct):
        if correct:
            self.current_question += 1
            self.next_question()
        else:
            self.end_game(f"Wrong answer! The correct answer was: {self.correct_answer}.\nYou leave with ${prizes[self.current_question - 1] if self.current_question > 0 else 0}.")

    def end_game(self, message):
        # Create a layout for the popup content
        popup_layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Game over message
        game_over_label = Label(text=message, font_size=20)
        popup_layout.add_widget(game_over_label)

        # Buttons layout
        buttons_layout = BoxLayout(orientation="horizontal", spacing=20)

        # Retry button
        retry_button = Button(text="Retry", font_size=20, background_color=(0, 0.5, 1, 1))
        retry_button.bind(on_press=self.retry_game)
        buttons_layout.add_widget(retry_button)

        # Exit to Menu button
        exit_button = Button(text="Exit to Menu", font_size=20, background_color=(1, 0, 0, 1))
        exit_button.bind(on_press=self.exit_to_menu)
        buttons_layout.add_widget(exit_button)

        # Add buttons to the popup layout
        popup_layout.add_widget(buttons_layout)

        # Create and open the popup
        popup = Popup(title="Game Over", content=popup_layout, size_hint=(0.75, 0.5), auto_dismiss=False)
        popup.open()

        # Store the popup reference for later dismissal
        self.game_over_popup = popup

    def retry_game(self, instance):
        # Close the game over popup
        self.game_over_popup.dismiss()

        # Reset game variables
        self.current_question = 0
        random.shuffle(questions)
        self.next_question()

    def exit_to_menu(self, instance):
        # Close the game over popup
        self.game_over_popup.dismiss()

        # Show the start screen with the Play button
        self.show_start_screen()  
    
if __name__ == "__main__":
    MillionaireApp().run()
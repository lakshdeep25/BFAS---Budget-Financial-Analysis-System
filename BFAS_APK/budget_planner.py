from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.uix.checkbox import CheckBox
import pandas as pd

class BudgetPlannerScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        self.create_layout()

    def create_layout(self):
        scroll_view = ScrollView()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Title Label
        layout.add_widget(MDLabel(
            text='Budget Planner',
            halign='center',
            theme_text_color='Primary',
            font_style='H4',
            size_hint=(1, None),
            height=50,
            color=get_color_from_hex('#4a148c')
        ))

        # Budget Input Fields
        self.income_field = MDTextField(
            hint_text='Enter Monthly Income (₹)',
            required=True,
            helper_text_mode='on_focus'
        )
        layout.add_widget(self.income_field)

        self.expenses_field = MDTextField(
            hint_text='Enter Monthly Expenses (₹)',
            required=True,
            helper_text_mode='on_focus'
        )
        layout.add_widget(self.expenses_field)

        # Financial Goals Input Fields
        self.goal_fields = {}
        goal_names = ['Car', 'House', 'Education', 'Emergency Fund', 'Wedding', 'Other']
        for goal in goal_names:
            self.goal_fields[goal] = MDTextField(
                hint_text=f'{goal} (₹)',
                required=False,
                helper_text_mode='on_focus'
            )
            layout.add_widget(self.goal_fields[goal])

        # Risk Level Checkboxes
        self.risk_levels = {
            'Stay Safe': False,
            'Small Risk': False,
            'High Risk': False
        }
        risk_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=150)
        self.risk_checkboxes = {}
        for risk in self.risk_levels.keys():
            checkbox = CheckBox(size_hint=(None, None), size=(48, 48))
            checkbox.color = (1, 1, 1, 1)  # Set checkbox color to white for visibility
            checkbox.bind(active=lambda checkbox, value, risk=risk: self.update_risk_level(risk, value))
            self.risk_checkboxes[risk] = checkbox
            risk_layout.add_widget(checkbox)
            risk_layout.add_widget(MDLabel(text=risk, theme_text_color='Secondary'))

        layout.add_widget(risk_layout)

        # Submit Button
        submit_button = MDRaisedButton(
            text='Submit Budget',
            size_hint=(None, None),
            width=200,
            height=50,
            pos_hint={'center_x': 0.5},
            on_release=self.submit_budget
        )
        layout.add_widget(submit_button)

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def update_risk_level(self, risk, value):
        self.risk_levels[risk] = value

    def submit_budget(self, _):
        try:
            income = float(self.income_field.text.strip())
            expenses = float(self.expenses_field.text.strip())
        except ValueError:
            self.show_popup('Error', 'Please enter valid numbers for income and expenses.')
            return

        remaining_income = income - expenses

        # Calculate total goal amount
        total_goal_amount = sum(float(field.text.strip() or 0) for field in self.goal_fields.values())

        # Check if no risk level was selected
        no_risk_selected = not any(self.risk_levels.values())

        result_text = f"Monthly Income: ₹{income}\nMonthly Expenses: ₹{expenses}\nRemaining Income: ₹{remaining_income}\nTotal Goal Amount: ₹{total_goal_amount}\n"
        if remaining_income >= total_goal_amount:
            result_text += f"\nCongratulations! You have enough funds to achieve your total goal amount.\n"
            result_text += "Continue with us to achieve even more financial goals!"
        else:
            result_text += "\nKeep saving to achieve your financial goals!"

        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        with popup_layout.canvas.before:
            Color(1, 1, 1, 1)  # Set background color to white
            self.rect = Rectangle(size=popup_layout.size, pos=popup_layout.pos)
            popup_layout.bind(size=self._update_rect, pos=self._update_rect)

        popup_layout.add_widget(Label(text=result_text, halign='center', size_hint_y=None, height=200, color=[0, 0, 0, 1]))  # Set text color to black
        continue_button = Button(text='Continue', size_hint=(None, None), width=200, height=50, pos_hint={'center_x': 0.5})
        popup_layout.add_widget(continue_button)

        popup = Popup(title='Budget Analysis Results', content=popup_layout, size_hint=(None, None), size=(400, 400))
        continue_button.bind(on_release=popup.dismiss)
        continue_button.bind(on_release=lambda x: self.go_to_new_screen(income, expenses, total_goal_amount, self.risk_levels, no_risk_selected))
        popup.open()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, halign='center'), size_hint=(None, None), size=(400, 200))
        popup.open()

    def go_to_new_screen(self, income, expenses, total_goal_amount, risk_levels, no_risk_selected):
        app = MDApp.get_running_app()
        app.show_results_screen(income, expenses, total_goal_amount, risk_levels, no_risk_selected)

class ResultsScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        self.create_layout()

    def create_layout(self):
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.layout)

        # Add ScrollView for recommendations
        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)
        self.scroll_layout = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        self.scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(self.scroll_view)

    # Create a layout for buttons with space above it
        button_container = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=100)
        button_container.add_widget(BoxLayout())  # Empty widget to push buttons to bottom

    # Create button layout for horizontal alignment
        button_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
    
    # "Let's Do It" Button
        lets_do_it_button = MDRaisedButton(
        text='Let\'s Do It',
        size_hint=(None, None),
        width=200,
        height=50,
        on_release=self.lets_do_it
    )
        button_layout.add_widget(lets_do_it_button)

    # "Let Know" Button
        let_know_button = MDRaisedButton(
        text='Let Know',
        size_hint=(None, None),
        width=200,
        height=50,
        on_release=self.let_know
    )
        button_layout.add_widget(let_know_button)

        button_container.add_widget(button_layout)
        self.layout.add_widget(button_container)

    def display_data(self, df, risk_levels):
        self.scroll_layout.clear_widgets()

        # Display the DataFrame as a Label
        data_str = df.to_string(index=False)
        self.scroll_layout.add_widget(MDLabel(text='Budget Planner Results:', halign='center', theme_text_color='Primary', font_style='H6'))

        self.scroll_layout.add_widget(MDLabel(text=data_str, halign='center'))

        # Display the selected risk levels
        risk_str = "Selected Risk Levels:\n"
        for risk, selected in risk_levels.items():
            risk_str += f"{risk}: {'Yes' if selected else 'No'}\n"
        self.scroll_layout.add_widget(MDLabel(text=risk_str, halign='center'))

    def lets_do_it(self, instance):
        # Define actions when "Let's Do It" button is clicked
        app = MDApp.get_running_app()
        app.show_sip_calculator_screen()

    def let_know(self, instance):
        # Define actions when "Let Know" button is clicked
        self.show_popup("Information", "Let Know button clicked.")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message, halign='center'), size_hint=(None, None), size=(400, 200))
        popup.open()

class SIPCalculatorScreen(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        self.create_layout()

    def create_layout(self):
        self.add_widget(MDLabel(
            text='SIP Calculator',
            halign='center',
            theme_text_color='Primary',
            font_style='H4',
            size_hint=(1, None),
            height=50,
            color=get_color_from_hex('#4a148c')
        ))

        # Add SIP Calculator fields and logic here

class BudgetPlannerApp(MDApp):
    def build(self):
        self.budget_planner_screen = BudgetPlannerScreen()
        self.results_screen = ResultsScreen()
        self.sip_calculator_screen = SIPCalculatorScreen()

        self.main_layout = MDBoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.budget_planner_screen)
        self.main_layout.add_widget(self.results_screen)
        self.main_layout.add_widget(self.sip_calculator_screen)

        self.show_budget_planner_screen()
        return self.main_layout

    def show_budget_planner_screen(self):
        self.budget_planner_screen.opacity = 1
        self.budget_planner_screen.disabled = False
        self.results_screen.opacity = 0
        self.results_screen.disabled = True
        self.sip_calculator_screen.opacity = 0
        self.sip_calculator_screen.disabled = True

    def show_results_screen(self, income, expenses, total_goal_amount, risk_levels, no_risk_selected):
        # Prepare and display the results data
        data = {
            'Income': [income],
            'Expenses': [expenses],
            'Total Goal Amount': [total_goal_amount],
            'No Risk Selected': [no_risk_selected]
        }
        df = pd.DataFrame(data)
        self.results_screen.display_data(df, risk_levels)

        self.budget_planner_screen.opacity = 0
        self.budget_planner_screen.disabled = True
        self.results_screen.opacity = 1
        self.results_screen.disabled = False
        self.sip_calculator_screen.opacity = 0
        self.sip_calculator_screen.disabled = True

    def show_sip_calculator_screen(self):
        self.budget_planner_screen.opacity = 0
        self.budget_planner_screen.disabled = True
        self.results_screen.opacity = 0
        self.results_screen.disabled = True
        self.sip_calculator_screen.opacity = 1
        self.sip_calculator_screen.disabled = False

if __name__ == '__main__':
    BudgetPlannerApp().run()

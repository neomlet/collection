import wikipedia
import random
import textwrap
from difflib import SequenceMatcher
import time
import colorama
from colorama import Fore, Style
import sqlite3
from threading import Timer
from pymorphy2 import MorphAnalyzer
import gettext
import os
from collections import defaultdict

colorama.init()
current_dir = os.path.dirname(os.path.abspath(__file__))
translations = gettext.translation('quiz', localedir=os.path.join(current_dir, 'locales'), languages=['en', 'ru', 'es', 'fr'])
translations.install()

class EnhancedQuiz(MultilingualQuiz):
    def __init__(self, lang='en'):
        super().__init__(lang)
        self.categories = self.load_categories()
        self.hints_used = 0
        self.game_stats = defaultdict(int)
        self.lives = 3
        self.current_category = None

    def load_categories(self):
        return {
            'general': _("General"),
            'science': _("Science"),
            'history': _("History"),
            'technology': _("Technology"),
            'culture': _("Culture")
        }

    def set_category(self):
        print(_("\n🎯 Choose category:"))
        for idx, (key, name) in enumerate(self.categories.items(), 1):
            print(f"{idx}. {name}")
        
        while True:
            choice = input("> ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.categories):
                self.current_category = list(self.categories.keys())[int(choice)-1]
                return
            print(_("Invalid choice. Try again."))

    def get_filtered_article(self):
        attempts = 0
        while attempts < 5:
            try:
                if self.current_category:
                    page = wikipedia.page(wikipedia.random(1, category=self.current_category))
                else:
                    page = wikipedia.page(wikipedia.random(1))
                
                content = page.content.split('\n')[0].strip()
                
                # Improved filtering
                if self.is_valid_content(content):
                    return content, page.title
            except Exception:
                pass
            attempts += 1
        return None, None

    def is_valid_content(self, content):
        # Exclude technical terms and rare topics
        blacklist = ['ISO', 'HTTP', 'DNA', 'RNA'] if self.lang == 'en' else []
        return (
            20 < len(content) < 150 and
            not any(word in content for word in blacklist) and
            content.count(' ') > 5 and
            ':' not in content
        )

    def show_hint(self, correct_answer):
        hint_cost = 50
        if self.total_score >= hint_cost:
            self.total_score -= hint_cost
            self.hints_used += 1
            hint = f"{correct_answer[0]}{'_'*(len(correct_answer)-1)}"
            print(_("\n💡 Hint: {}").format(hint))
        else:
            print(_("\n❌ Not enough points for hint!"))

    def ask_question(self):
        question, correct, title = self.generate_question()
        if not question:
            return False
            
        print(f"\n{Fore.CYAN}📚 {_('Topic')}: {title}{Style.RESET_ALL}")
        print(textwrap.fill(question, width=80) + "\n")
        
        timer = Timer(self.time_limit, self.timer_expired)
        timer.start()
        
        start_time = time.time()
        while True:
            user_input = input(f"{Fore.GREEN}✎ {_('Your answer')} (h for hint): {Style.RESET_ALL}").strip()
            if user_input.lower() == 'h':
                self.show_hint(correct)
                continue
            break
        
        elapsed = time.time() - start_time
        timer.cancel()
        
        if self.check_answer(user_input, correct):
            points = self.calculate_points(elapsed, correct)
            self.update_stats(True, points)
        else:
            self.lives -= 1
            self.update_stats(False)
            print(f"{Fore.RED}✗ {_('Wrong. Correct answer')}: {correct}{Style.RESET_ALL}")
            if self.lives <= 0:
                print(f"{Fore.RED}💔 {_('No lives left!')}{Style.RESET_ALL}")
                return False
        
        return True

    def calculate_points(self, elapsed_time, correct_answer):
        base_points = 100
        time_bonus = max(0, 300 - int(elapsed_time * 100))
        length_bonus = len(correct_answer) * 10
        streak_bonus = self.streak * 20
        return base_points + time_bonus + length_bonus + streak_bonus

    def update_stats(self, correct, points=0):
        self.game_stats['total_questions'] += 1
        if correct:
            self.game_stats['correct_answers'] += 1
            self.total_score += points
            self.streak += 1
        else:
            self.game_stats['wrong_answers'] += 1
            self.streak = 0

    def show_stats(self):
        print(_("\n📊 Game Statistics:"))
        print(_("✓ Correct answers: {}").format(self.game_stats['correct_answers']))
        print(_("✗ Wrong answers: {}").format(self.game_stats['wrong_answers']))
        print(_("🔥 Longest streak: {}").format(self.streak))
        print(_("💡 Hints used: {}").format(self.hints_used))
        print(_("⏱️ Average time: {:.1f}s").format(
            self.game_stats['total_time'] / self.game_stats['total_questions']
            if self.game_stats['total_questions'] > 0 else 0
        ))

    def start_game(self):
        self.set_language()
        self.setup_wikipedia()
        self.set_category()
        self.set_difficulty()
        
        print(_("\n🌟 Welcome to Enhanced Quiz! 🌟"))
        username = input(_("\nEnter your name: ")).strip()
        
        while self.lives > 0:
            if not self.ask_question():
                break
                
            cont = input(_("\n▶ Continue? (y/n): ")).lower()
            if cont not in ['y', 'д']:
                break
        
        print(_("\n✨ Game Over! Final score: {}").format(self.total_score))
        self.show_stats()
        self.save_result(username)
        self.show_leaderboard()

if __name__ == "__main__":
    game = EnhancedQuiz()
    game.start_game()
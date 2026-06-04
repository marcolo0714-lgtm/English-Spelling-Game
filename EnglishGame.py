import os
import random
import time
import threading
import tempfile
import pygame
import json

try:
    from gtts import gTTS
    _HAS_GTTS = True
except Exception:
    _HAS_GTTS = False



def load_words(level):
    """Load the word list for the specified difficulty level.
    Args:
        level (int): The KS level number to load (1-4).
    Returns:
        list[str]: A list of non-empty words read from the KS file.
    """
    fname = f"word_folder/KS{level}_words.json"

    with open(fname, 'r', encoding='utf-8') as f:
        list_of_words = json.load(f)
        return list_of_words


class TTSPlayer:
    def __init__(self):
        """Initialize the text-to-speech helper.
        Attempts to initialize the pygame audio mixer and configures the
        TTS engine availability state.
        """
        # Initialize the pygame mixer only if the environment supports audio playback.
        try:
            pygame.mixer.init()
        except Exception:
            pass
        # Placeholder for a speech engine object if future support is added.

    def speak(self, text):
        """Speak the given text aloud or print a fallback message.
        If gTTS is available, this method starts a background thread to play
        the generated audio so the UI remains responsive.
        """
        if not text:
            return
        if _HAS_GTTS:
            try:
                # Use a background thread so audio generation and playback do not
                # block the main game loop.
                thr = threading.Thread(target=self._speak_gtts, args=(text,), daemon=True)
                thr.start()
                return
            except Exception:
                pass

        # Fallback output when the TTS library is unavailable.
        print('(TTS unavailable) Word:', text)

    def _speak_gtts(self, text):
        """Generate and play TTS audio for the provided English text."""
        try:
            tts = gTTS(text=text, lang='en')
            # Create a temporary file to store the spoken MP3 audio.
            tf = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tf.close()
            path = tf.name
            tts.save(path)
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            finally:
                try:
                    os.remove(path)
                except Exception:
                    pass
        except Exception:
            pass


class EnglishGame:
    def __init__(self):
        """Initialize the game state, window, fonts, and audio helper."""
        pygame.init()
        self.screen = pygame.display.set_mode((900, 520))
        pygame.display.set_caption('English Spelling Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 32)
        self.large_font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)

        # Current selected learning level (1-4), or None if not chosen.
        self.level = None
        # List of words (each word is a dictionary) loaded for the current level.
        self.words = []
        # The word currently being spelled in this round.
        self.current_word = None
        # The string typed by the player as their answer.
        self.typed = ''
        # Feedback message shown in the UI.
        self.message = ''
        # Number of correct answers.
        self.score = 0
        # Total number of rounds played.
        self.rounds = 0
        # Seconds allowed for each spelling attempt.
        self.time_limit = 20
        # Time when the current round started.
        self.start_time = None
        # Whether a word is currently active and waiting for input.
        self.active = False
        # Text-to-speech helper used to pronounce words.
        self.tts = TTSPlayer()

    def draw_text(self, text, pos, font=None, color=(0, 0, 0)):
        """Render text onto the main game surface at the given position."""
        if font is None:
            font = self.font
        while text:
            next_draw = text.split('\n', 1)[0]
            surf = font.render(next_draw, True, color)
            self.screen.blit(surf, pos)

            text = text[len(next_draw):].lstrip()
            pos = (pos[0], pos[1] + surf.get_height())

    def choose_word(self):
        """Pick a random word from the currently loaded word list."""
        if not self.words:
            return None
        return random.choice(self.words)

    def start_round(self):
        """Begin a new round by selecting a word and starting the timer."""
        self.current_word = self.choose_word()
        if not self.current_word:
            self.message = 'No words available for this level.'
            self.active = False
            return
        self.typed = ''
        self.message = f'Definition: [{self.current_word["pos"]}] {self.current_word["def"]}'
        self.message = self._wrap_text(self.message, 75)  # Wrap message text to fit within a certain width
        self.start_time = time.time()
        self.active = True
        self.rounds += 1
        self.tts.speak(self.current_word["word"])
    
    def _wrap_text(self, text, max_line_length):
        """Wrap the input text into multiple lines based on a maximum line length."""
        words = text.split()
        lines = []
        current_line = ''
        for word in words:
            if len(current_line) + len(word) + 1 <= max_line_length:
                current_line += (' ' if current_line else '') + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return '\n'.join(lines)
    
    def submit_answer(self):
        """Validate the typed answer and update score, feedback, and round state."""
        if not self.current_word["word"]:
            return
        correct = self.typed.strip().lower() == self.current_word["word"].lower()
        if correct:
            self.score += 1
            self.message = f'Correct! (Also accepted: {self.current_word["alter"]})' if self.current_word.get('alter') and self.current_word['alter'] != "nan" else 'Correct!'
        elif (self.current_word.get('alter') and self.typed.strip().lower() == self.current_word['alter'].lower()):
            self.score += 1
            self.message = f'Correct! (Also accepted: {self.current_word["word"]})'
        else:
            self.message = f'Wrong. Correct word: {self.current_word["word"]}'
            if self.current_word.get('alter') != "nan":
                self.message += f'\n(Also accepted: {self.current_word["alter"]})'
        self.active = False

    def run(self):
        """Run the main game loop, handle player input, and render the UI."""

        # Define layout of screen (vertical positions of buttons and texts)
        first_text_height = 20
        first_row_button_height = 60
        second_row_button_height = 130
        second_text_height = 210
        input_box_height = 260
        message_height = 320
        third_text_height = 400
        third_row_button_height = 440

        # Prepare buttons positions and sizes
        buttons = []
        for i in range(4):
            rect = pygame.Rect(50 + i * 200, first_row_button_height, 160, 50)
            buttons.append((rect, f'KS{i+1}'))

        next_button = pygame.Rect(50, second_row_button_height, 220, 50)
        rehear_button = pygame.Rect(320, second_row_button_height, 220, 50)
        exit_button = pygame.Rect(590, second_row_button_height, 220, 50)
        reset_button = pygame.Rect(50, third_row_button_height, 220, 50)

        k_width, k_height = 60, 60  # standard size for key icons
        k_arrow_up = pygame.image.load("key_button_image/arrow-up.png").convert_alpha()
        k_arrow_down = pygame.image.load("key_button_image/arrow-down.png").convert_alpha()
        k_arrow_left = pygame.image.load("key_button_image/arrow-left.png").convert_alpha()
        k_arrow_right = pygame.image.load("key_button_image/arrow-right.png").convert_alpha()
        k_space = pygame.image.load("key_button_image/space.png").convert_alpha()
        k_backspace = pygame.image.load("key_button_image/backspace.png").convert_alpha()
        k_esc = pygame.image.load("key_button_image/esc.png").convert_alpha()
        k_enter = pygame.image.load("key_button_image/enter.png").convert_alpha()
        k_arrow_up = pygame.transform.scale(k_arrow_up, (k_width, k_height))
        k_arrow_down = pygame.transform.scale(k_arrow_down, (k_width, k_height))
        k_arrow_left = pygame.transform.scale(k_arrow_left, (k_width, k_height))
        k_arrow_right = pygame.transform.scale(k_arrow_right, (k_width, k_height))
        k_space = pygame.transform.scale(k_space, (k_width, k_height))
        k_backspace = pygame.transform.scale(k_backspace, (k_width, k_height))
        k_esc = pygame.transform.scale(k_esc, (k_width, k_height))
        k_enter = pygame.transform.scale(k_enter, (k_width, k_height))

        # Main loop
        running = True
        while running:
            self.screen.fill((240, 240, 240))
            mx, my = pygame.mouse.get_pos()

            # Event handling (mouse clicks, key presses)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for idx, (rect, label) in enumerate(buttons):  # if click on level buttons
                        if rect.collidepoint(event.pos):
                            self.level = idx + 1
                            self.words = load_words(self.level)
                    if next_button.collidepoint(event.pos):        # click on Next
                        if self.level and not self.active:
                            self.start_round()
                    if rehear_button.collidepoint(event.pos):      # click on Rehear
                        if self.current_word:
                            self.tts.speak(self.current_word["word"])
                    if exit_button.collidepoint(event.pos):        # click on Exit
                        running = False
                    if reset_button.collidepoint(event.pos):       # click on Reset
                        # reset score
                        if self.level and not self.active:
                            self.score = 0
                            self.rounds = 0
                            self.message = 'Score reset.'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:            # handle backspace
                        self.typed = self.typed[:-1]
                    elif event.key == pygame.K_RETURN:             # handle Enter key to submit answer
                        if self.active:
                            self.submit_answer()
                    elif event.key == pygame.K_LEFT:               # handle left arrow to decrease level
                        if self.level and not self.active:
                            self.level = max(1, self.level - 1)
                            self.words = load_words(self.level)
                    elif event.key == pygame.K_RIGHT:              # handle right arrow to increase level
                        if self.level and not self.active:
                            self.level = min(4, self.level + 1)
                            self.words = load_words(self.level)
                    elif event.key == pygame.K_SPACE:              # handle space to start next round
                        if self.level and not self.active:
                            self.start_round()
                    elif event.key == pygame.K_UP:                 # handle up arrow to rehear word
                        if self.current_word:
                            self.tts.speak(self.current_word["word"])
                    elif event.key == pygame.K_DOWN:               # handle down arrow to reset score
                        if self.level and not self.active:
                            self.score = 0
                            self.rounds = 0
                            self.message = 'Score reset.'
                    elif event.key == pygame.K_ESCAPE:             # handle Esc key to exit
                        running = False
                    else:
                        if self.active:                            # handle regular character input for typing the answer
                            if len(self.typed) < 60:
                                self.typed += event.unicode

            # Draw UI
            # 1st row text
            if self.level is None:
                self.draw_text('Select level:', (50, first_text_height), self.font)
            elif self.active:
                self.draw_text(f'Listen and type the word:', (50, first_text_height), self.font)
            else:
                self.draw_text(f'Select level (or use                         keys): KS{self.level} ({len(self.words)} words)', (50, first_text_height), self.font)

            # Draw 1st row (level) buttons with hover effect
            for rect, label in buttons:
                color = (180, 180, 255) if self.level and label == f'KS{self.level}' else (200, 200, 200)
                if rect.collidepoint((mx, my)):
                    pygame.draw.rect(self.screen, (150, 150, 255), rect)
                else:
                    pygame.draw.rect(self.screen, color, rect)
                self.draw_text(label, (rect.x + 20, rect.y + 12), self.font)
            
            # Draw 2nd row buttons appear or not based on game state, with hover effects
            hover_next = next_button.collidepoint((mx, my))
            hover_rehear = rehear_button.collidepoint((mx, my))
            hover_exit = exit_button.collidepoint((mx, my))
            hover_reset = reset_button.collidepoint((mx, my))

            if self.level is not None:  # only draw after a level is selected
                if not self.active:
                    pygame.draw.rect(self.screen, (160, 255, 160) if not hover_next else (120, 230, 120), next_button)
                    self.draw_text('Next', (next_button.x + 28, next_button.y + 12), self.font)
                    pygame.draw.rect(self.screen, (220, 220, 255) if not hover_reset else (190, 190, 255), reset_button)
                    self.draw_text('Reset score', (reset_button.x + 12, reset_button.y + 10), self.font)
                pygame.draw.rect(self.screen, (255, 200, 100) if not hover_rehear else (220, 170, 60), rehear_button)
                self.draw_text('Rehear', (rehear_button.x + 20, rehear_button.y + 12), self.font)
            pygame.draw.rect(self.screen, (255, 160, 160) if not hover_exit else (220, 120, 120), exit_button)
            self.draw_text('Exit', (exit_button.x + 32, exit_button.y + 12), self.font)
            

            # Draw small key icons near buttons based on the current game state
            if self.level is not None:  # only draw after a level is selected
                self.screen.blit(k_arrow_up, (470, second_row_button_height - 5))   # Up arrow near Rehear
                if not self.active:
                    self.screen.blit(k_arrow_left, (260, first_text_height - 20))   # Left arrow near KS level
                    self.screen.blit(k_arrow_right, (330, first_text_height - 20))  # Right arrow near KS level
                    self.screen.blit(k_space, (200, second_row_button_height - 5))  # Space near Next
                    self.screen.blit(k_arrow_down, (200, third_row_button_height - 5)) # Down arrow near Reset score
                else:
                    self.screen.blit(k_backspace, (660, input_box_height - 10))     # Backspace near input box
                    self.screen.blit(k_enter, (720, input_box_height - 10))         # Enter near input box
            self.screen.blit(k_esc, (740, second_row_button_height - 5))            # Esc near Exit

            # Game info
            self.draw_text(f'Score: {self.score}/{self.rounds}', (50, third_text_height), self.font)

            if self.active and self.start_time:
                remaining = int(self.time_limit - (time.time() - self.start_time))
                if remaining < 0:
                    remaining = 0
                self.draw_text(f'Time left: {remaining}s', (50, 200), self.large_font)
                if remaining == 0:
                    self.message = f'Time up — correct: {self.current_word["word"]}'
                    self.active = False
            elif self.level is None:
                self.draw_text('Select a level to start the game.', (50, second_text_height), self.font)
            else:
                self.draw_text('Press Space or click Next to hear a word.', (50, second_text_height), self.font)

            # Input box
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, input_box_height, 600, 40))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(50, input_box_height, 600, 40), 2)
            self.draw_text(self.typed, (60, input_box_height + 8), self.font)

            # Message
            self.draw_text(self.message, (50, message_height), self.font, color=(80, 80, 80) if self.message != 'Correct!' else (0, 150, 0))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


def main():
    """Create the game instance and start the main loop."""
    game = EnglishGame()
    game.run()


if __name__ == '__main__':
    main()

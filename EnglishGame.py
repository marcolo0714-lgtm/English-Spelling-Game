import os
import sys
import random
import time
import threading
import tempfile
import pygame


try:
	from gtts import gTTS
	_HAS_GTTS = True
except Exception:
	_HAS_GTTS = False


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_FOLDER = os.path.join(BASE_DIR, 'word_folder')


def load_words(level):
	fname = os.path.join(WORD_FOLDER, f'KS{level}_words.txt')
	if not os.path.exists(fname):
		return []
	with open(fname, 'r', encoding='utf-8') as f:
		return [line.strip() for line in f if line.strip()]


class TTSPlayer:
	def __init__(self):
		pygame.mixer.init()
		self.engine = None
		if not _HAS_GTTS:
			self.engine = None

	def speak(self, text):
		if _HAS_GTTS:
			try:
				t = threading.Thread(target=self._speak_gtts, args=(text,), daemon=True)
				t.start()
				return
			except Exception:
				pass

		print('(TTS unavailable) Word:', text)


	def _speak_gtts(self, text):
		try:
			tts = gTTS(text=text, lang='en')
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
		pygame.init()
		self.screen = pygame.display.set_mode((900, 450))
		pygame.display.set_caption('English Spelling Game')
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont(None, 32)
		self.large_font = pygame.font.SysFont(None, 48)
		self.small_font = pygame.font.SysFont(None, 24)

		self.level = None
		self.words = []
		self.current_word = None
		self.typed = ''
		self.message = ''
		self.score = 0
		self.rounds = 0
		self.time_limit = 20
		self.start_time = None
		self.active = False
		self.tts = TTSPlayer()

	def draw_text(self, text, pos, font=None, color=(0, 0, 0)):
		if font is None:
			font = self.font
		surf = font.render(text, True, color)
		self.screen.blit(surf, pos)

	def choose_word(self):
		if not self.words:
			return None
		return random.choice(self.words)

	def start_round(self):
		self.current_word = self.choose_word()
		if not self.current_word:
			self.message = 'No words available for this level.'
			self.active = False
			return
		self.typed = ''
		self.message = ''
		self.start_time = time.time()
		self.active = True
		self.rounds += 1
		self.tts.speak(self.current_word)

	def submit_answer(self):
		if not self.current_word:
			return
		correct = self.typed.strip().lower() == self.current_word.lower()
		if correct:
			self.score += 1
			self.message = 'Correct!'
		else:
			self.message = f'Wrong — correct: {self.current_word}'
		self.active = False

	def run(self):
		buttons = []
		for i in range(4):
			rect = pygame.Rect(50 + i * 200, 50, 160, 50)
			buttons.append((rect, f'KS{i+1}'))

		next_button = pygame.Rect(50, 120, 220, 50)
		rehear_button = pygame.Rect(320, 120, 220, 50)
		exit_button = pygame.Rect(590, 120, 220, 50)
		reset_button = pygame.Rect(50, 360, 220, 50)

		running = True
		while running:
			self.screen.fill((240, 240, 240))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					mx, my = event.pos
					for idx, (rect, label) in enumerate(buttons):
						if rect.collidepoint(mx, my):
							self.level = idx + 1
							self.words = load_words(self.level)
					if next_button.collidepoint(mx, my) and self.level and not self.active:
						self.start_round()
					if rehear_button.collidepoint(mx, my):
						self.tts.speak(self.current_word)
					if exit_button.collidepoint(mx, my):
						running = False
					if reset_button.collidepoint(mx, my) and self.level and not self.active:
						self.score = 0
						self.rounds = 0
						self.message = 'Score reset.'
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_BACKSPACE:
						self.typed = self.typed[:-1]
					elif event.key == pygame.K_RETURN:
						if self.active:
							self.submit_answer()
					elif event.key == pygame.K_LEFT:
						if self.level and not self.active:
							self.level = max(1, self.level - 1)
							self.words = load_words(self.level)
					elif event.key == pygame.K_RIGHT:
						if self.level and not self.active:
							self.level = min(4, self.level + 1)
							self.words = load_words(self.level)
					elif event.key == pygame.K_SPACE:
						if self.level and not self.active:
							self.start_round()
					elif event.key == pygame.K_UP:
						self.tts.speak(self.current_word)
					elif event.key == pygame.K_ESCAPE:
						running = False
					else:
						if self.active:
							# limit input length
							if len(self.typed) < 60:
								self.typed += event.unicode

			# Draw UI
			if self.level == None:
				self.draw_text('Select level:', (50, 20), self.font)
			else:
				self.draw_text(f'Select level (or use Left/Right keys): KS{self.level} ({len(self.words)} words)', (50, 20), self.font)
			for rect, label in buttons:
				color = (180, 180, 255) if self.level and label == f'KS{self.level}' else (200, 200, 200)
				pygame.draw.rect(self.screen, color, rect)
				self.draw_text(label, (rect.x + 20, rect.y + 12), self.font)

			pygame.draw.rect(self.screen, (160, 255, 160), next_button)
			self.draw_text('Next ␣', (next_button.x + 20, next_button.y + 12), self.font)
			pygame.draw.rect(self.screen, (255, 200, 100), rehear_button)
			self.draw_text('Rehear ↑', (rehear_button.x + 20, rehear_button.y + 12), self.font)
			pygame.draw.rect(self.screen, (255, 160, 160), exit_button)
			self.draw_text('Exit Esc', (exit_button.x + 20, exit_button.y + 12), self.font)
			pygame.draw.rect(self.screen, (220, 220, 255), reset_button)
			self.draw_text('Reset score', (reset_button.x + 12, reset_button.y + 10), self.font)

			# Game info
			self.draw_text(f'Score: {self.score}/{self.rounds}', (50, 320), self.font)

			if self.active and self.start_time:
				remaining = int(self.time_limit - (time.time() - self.start_time))
				if remaining < 0:
					remaining = 0
				self.draw_text(f'Time left: {remaining}s', (50, 200), self.large_font)
				if remaining == 0:
					self.message = f'Time up — correct: {self.current_word}'
					self.active = False
			elif self.level == None:
				self.draw_text('Select a level to start the game.', (50, 200), self.font)
			else:
				self.draw_text('Press Space or click Next to hear a word.', (50, 200), self.font)
			# Input box
			pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(50, 240, 600, 40))
			pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(50, 240, 600, 40), 2)
			self.draw_text(self.typed, (60, 248), self.font)

			# Message
			self.draw_text(self.message, (50, 290), self.font, color=(80, 80, 80))

			pygame.display.flip()
			self.clock.tick(30)

		pygame.quit()


def main():
	game = EnglishGame()
	game.run()


if __name__ == '__main__':
	main()


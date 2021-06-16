import pygame


class InputBox:

    def __init__(self, game, x, y, w, h, text=''):
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.color = game.white
        self.text = text
        self.txt_surface = game.font_name.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        # for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.game.green if self.active else self.game.red
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    score = (self.text, self.game.gameplay.score)
                    self.game.ranks.insert_score(score)
                    self.text = ''
                    self.game.rank_table = self.game.ranks.get_data()
                    self.game.switch_display(self.game.main)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.game.font_name.render(
                    self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

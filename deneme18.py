import pygame
import sys
import math

pygame.init()

# Ekranı tam ekran modunda aç
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

pygame.display.set_caption("Kriptarium Tangram")

# Renkler
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (173, 216, 230)
yellow = (255, 255, 0)

# Şekil boyutları ve ölçekleri
shape_size = 80
enlarged_scale = 1.5
enlarged_blue_scale = 1.25
rotation_speed = 2

# Diğer ölçümler
tri_height = int(shape_size * math.sqrt(3) / 2)
inner_tri_height = int(tri_height / 2)
inner_tri_width = int(tri_height / math.sqrt(3))

# Şekil listesi
shapes = []

class Shape:
    def __init__(self, x, y, shape_type, color, scale=1):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.angle = 0
        self.color = color
        self.scale = scale

    def draw(self):
        scaled_size = shape_size * self.scale
        if self.shape_type == "square" or self.shape_type == "parallelogram":
            rotated_shape = pygame.transform.rotate(pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA), self.angle)
            rotated_shape.fill((0, 0, 0, 0))
            pygame.draw.rect(rotated_shape, self.color, (0, 0, scaled_size, scaled_size))
            rotated_shape = pygame.transform.rotate(rotated_shape, self.angle)
            new_rect = rotated_shape.get_rect(center=(self.x, self.y))
            screen.blit(rotated_shape, new_rect.topleft)
        elif self.shape_type == "triangle":
            rotated_triangle = []
            points = [(self.x + scaled_size / 2, self.y - scaled_size / 2), (self.x, self.y + scaled_size / 2), (self.x + scaled_size, self.y + scaled_size / 2)]
            for point in points:
                x, y = point
                x_rotated = (x - points[1][0]) * math.cos(math.radians(self.angle)) - (y - points[1][1]) * math.sin(math.radians(self.angle)) + points[1][0]
                y_rotated = (x - points[1][0]) * math.sin(math.radians(self.angle)) + (y - points[1][1]) * math.cos(math.radians(self.angle)) + points[1][1]
                rotated_triangle.append((x_rotated, y_rotated))
            pygame.draw.polygon(screen, self.color, rotated_triangle)

# Şekil örnekleri oluştur
shapes.append(Shape(100, 300, "triangle", red))  # Kırmızı üçgen
shapes.append(Shape(220, 300, "triangle", green, scale=enlarged_scale))  # %50 büyütülmüş yeşil üçgen
shapes.append(Shape(340, 300, "triangle", blue, scale=enlarged_blue_scale))  # %25 büyütülmüş mavi üçgen
shapes.append(Shape(460, 300, "square", light_blue))  # Kırmızı kare (önceki üçgen)
shapes.append(Shape(580, 300, "triangle", green, scale=enlarged_scale))  # %50 büyütülmüş yeşil üçgen
shapes.append(Shape(700, 300, "triangle", red))  # Kırmızı üçgen
shapes.append(Shape(880, 300, "parallelogram", yellow))

# Yazı ve simge ayarları
font = pygame.font.Font(None, 72)
text_surface = font.render("Kriptarium Tangram", True, (0, 0, 0))
text_rect = text_surface.get_rect(midtop=(screen_width // 2, 10))
icon = pygame.image.load("kriptarium.jpg")
icon = pygame.transform.scale(icon, (72, 72))

# Oyun döngüsü
clock = pygame.time.Clock()

running = True
dragging = False
selected_shape = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for shape in shapes:
                    distance = math.sqrt((event.pos[0] - shape.x)**2 + (event.pos[1] - shape.y)**2)
                    if distance <= shape_size / 2 * shape.scale:
                        dragging = True
                        selected_shape = shape
                        mouse_offset_x = event.pos[0] - shape.x
                        mouse_offset_y = event.pos[1] - shape.y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                selected_shape = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging and selected_shape:
                selected_shape.x = event.pos[0] - mouse_offset_x
                selected_shape.y = event.pos[1] - mouse_offset_y
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if selected_shape:
                    selected_shape.angle += rotation_speed
            elif event.key == pygame.K_RIGHT:
                if selected_shape:
                    selected_shape.angle -= rotation_speed
            elif event.key == pygame.K_q:  # 'q' tuşuna basarak çıkış
                running = False

    screen.fill((255, 255, 255))

    for shape in shapes:
        shape.draw()

    screen.blit(icon, (text_rect.right + 10, text_rect.centery - icon.get_height() // 2))
    screen.blit(text_surface, text_rect.topleft)

    # Çıkış butonunu göster
    quit_text = font.render("Çıkış için 'q'", True, (0, 0, 0))
    screen.blit(quit_text, (10, screen_height - quit_text.get_height() - 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

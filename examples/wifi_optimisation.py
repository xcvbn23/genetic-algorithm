import math
import statistics
import pygame

from genetic_algorithm import GeneticAlgorithm, REPLACEMENT_METHOD


def slope(p1, p2):
    return (p2[1] - p1[1]) * 1.0 / (p2[0] - p1[0])


def y_intercept(slope, p1):
    return p1[1] - 1.0 * slope * p1[0]


def intersect(line1, line2):
    min_allowed = 1e-5  # guard against overflow
    big_value = 1e10  # use instead (if overflow would have occurred)
    m1 = slope(line1[0], line1[1])
    print("m1: %d" % m1)
    b1 = y_intercept(m1, line1[0])
    print("b1: %d" % b1)
    m2 = slope(line2[0], line2[1])
    print("m2: %d" % m2)
    b2 = y_intercept(m2, line2[0])
    print("b2: %d" % b2)
    if abs(m1 - m2) < min_allowed:
        x = big_value
    else:
        x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    y2 = m2 * x + b2
    print("(x,y,y2) = %d,%d,%d" % (x, y, y2))
    return (int(x), int(y))


def segment_intersect(line1, line2):
    # https://www.codeproject.com/Tips/864704/Python-Line-Intersection-for-Pygame
    intersection_pt = intersect(line1, line2)

    print(line1[0][0], line1[1][0], line2[0][0], line2[1][0], intersection_pt[0])
    print(line1[0][1], line1[1][1], line2[0][1], line2[1][1], intersection_pt[1])

    if line1[0][0] < line1[1][0]:
        if intersection_pt[0] < line1[0][0] or intersection_pt[0] > line1[1][0]:
            print("exit 1")
            return None
    else:
        if intersection_pt[0] > line1[0][0] or intersection_pt[0] < line1[1][0]:
            print("exit 2")
            return None

    if line2[0][0] < line2[1][0]:
        if intersection_pt[0] < line2[0][0] or intersection_pt[0] > line2[1][0]:
            print("exit 3")
            return None
    else:
        if intersection_pt[0] > line2[0][0] or intersection_pt[0] < line2[1][0]:
            print("exit 4")
            return None

    return intersection_pt


pygame.init()
pygame.display.set_caption("Line of Sight")
display_win = pygame.display.set_mode([500, 500])
win = pygame.Surface((100, 100))


WHITE = (200, 200, 200)
GREY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
TAN = (240, 171, 15)
YELLOW = (255, 255, 0)


class Being(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, colour=YELLOW, size=5):
        pygame.sprite.Sprite.__init__(self)
        self.colour = colour
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = size
        self.seen = False
        self.update()

    def update(self):
        """If we've been seen, go red with embrassment"""
        if self.seen:
            colour = RED
        else:
            colour = self.colour
        pygame.draw.circle(
            self.image, colour, (self.size // 2, self.size // 2), self.size // 2
        )

    def setSeen(self, seen=True):
        self.seen = seen

    def getCentre(self):
        return self.rect.center

    def getRect(self):
        return self.rect


# Users
users = [(0, 0), (100, 100)]
user_sprites = pygame.sprite.Group()
for user_location in users:
    user_sprites.add(Being(*user_location, GREEN))
user_sprites.update()
user_sprites.draw(win)

# Routers
player_sprite = pygame.sprite.GroupSingle()
player = Being(0, 0)  # bottom middle
player_sprite.add(player)

# Walls
walls = [[(75, 50), (100, 50)]]


def freespace_propagation_loss(distance: float, frequency: float):
    # frequency is frequency(Hz)
    # distance is meters(m)
    light_speed = 300000000.0  # m/s
    return 20 * math.log10((4.0 * math.pi * distance) / (light_speed / frequency))


class WifiOptimisationGeneticAlgorithm(GeneticAlgorithm):
    def gene_definition(self):
        return [(int, 1, 1), (float, 0, 100), (float, 0, 100)]

    def fitness_func(self, gene: list) -> float:
        path_losses = []
        for user in users:
            distance = math.dist(user, gene[1:])
            path_loss = freespace_propagation_loss(distance, 2.412 * math.pow(10, 9))
            if path_loss > 85:
                return -999
            path_losses.append(path_loss)

        total_path_loss = sum(path_losses)
        path_loss_variance = statistics.variance(path_losses)

        return -path_loss_variance - total_path_loss

    def generations(self):
        return 500

    def mutation_rate(self) -> float:
        return 0.05

    def num_of_parents(self):
        return 10

    def on_complete(self, best_individuals: list) -> None:
        super().on_complete(best_individuals)
        _, best_gene, _ = best_individuals[0]
        [_, router_x, router_y] = best_gene

        win.fill(BLACK)

        user_sprites.draw(win)

        player.rect.x = router_x
        player.rect.y = router_y
        player_sprite.draw(win)

        for wall in walls:
            pygame.draw.line(win, TAN, *wall)

        for user in users:
            for wall in walls:
                router_user = [(router_x, router_y), user]
                print(segment_intersect(wall, router_user))
                pygame.draw.line(win, RED, *router_user)

        scaled_win = pygame.transform.smoothscale(win, display_win.get_size())
        display_win.blit(scaled_win, (0, 0))
        pygame.display.flip()

    def population_size(self):
        return 100

    def replacement_method(self) -> REPLACEMENT_METHOD:
        return REPLACEMENT_METHOD.WEAK_PARENT


if __name__ == "__main__":
    genetic_algorithm = WifiOptimisationGeneticAlgorithm()
    genetic_algorithm.run()
    pygame.image.save(display_win, "screenshot.jpg")
    pygame.quit()

import math
import statistics
import pygame

pygame.init()
pygame.display.set_caption("Line of Sight")

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


window = pygame.display.set_mode([100, 100])

# Routers
player_sprite = pygame.sprite.GroupSingle()
player = Being(0, 0)  # bottom middle
player_sprite.add(player)

# Users
users = [(0, 0), (100, 100)]
user_sprites = pygame.sprite.Group()
for user_location in users:
    user_sprites.add(Being(*user_location, GREEN))
user_sprites.update()


def freespace_propagation_loss(distance: float, frequency: float):
    # frequency is frequency(Hz)
    # distance is meters(m)
    light_speed = 300000000.0  # m/s
    return 20 * math.log10((4.0 * math.pi * distance) / (light_speed / frequency))


from genetic_algorithm import REPLACEMENT_METHOD, GeneticAlgorithm


class WifiOptimisationGeneticAlgorithm(GeneticAlgorithm):
    def gene_definition(self):
        return [(int, 1, 1), (float, 0, 100), (float, 0, 100)]

    def fitness_func(self, gene: list) -> float:
        distances = []
        path_losses = []
        for user in users:
            distance = math.dist(user, gene[1:])
            distances.append(distance)
            path_loss = freespace_propagation_loss(distance, 2.412 * math.pow(10, 9))
            # if path_loss > 80:
            #     return -999
            path_losses.append(path_loss)

        total_path_loss = sum(path_losses)
        path_loss_variance = statistics.variance(path_losses)

        [_, x, y] = gene

        window.fill(BLACK)

        user_sprites.draw(window)

        player.rect.x = x
        player.rect.y = y
        player_sprite.draw(window)

        pygame.display.flip()

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
        [_, x, y] = best_gene

        window.fill(BLACK)

        user_sprites.draw(window)
        player.rect.x = x
        player.rect.y = y
        player_sprite.draw(window)

        pygame.display.flip()

    def population_size(self):
        return 100

    def replacement_method(self) -> REPLACEMENT_METHOD:
        return REPLACEMENT_METHOD.WEAK_PARENT


if __name__ == "__main__":
    genetic_algorithm = WifiOptimisationGeneticAlgorithm()
    genetic_algorithm.run()
    pygame.image.save(window, "screenshot.jpg")
    pygame.quit()

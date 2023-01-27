import math
import statistics

import pygame

from examples.wifi_optimisation_utils import (
    freespace_propagation_loss,
    segment_intersect,
)
from genetic_algorithm import REPLACEMENT_METHOD, GeneticAlgorithm

users = [(0, 50), (100, 50)]
walls = [[(75, 0), (75, 75)]]


class WifiOptimisationGeneticAlgorithm(GeneticAlgorithm):
    def gene_definition(self):
        return [(int, 1, 1), (float, 0, 100), (float, 0, 100)]

    def fitness_func(self, gene: list) -> float:
        path_losses = []

        router = gene[1:]

        for user in users:
            distance = math.dist(user, router)
            path_loss = freespace_propagation_loss(distance, 2.412 * math.pow(10, 9))
            for wall in walls:
                if segment_intersect(wall, [router, user]):
                    path_loss += 3

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

        pygame.init()
        pygame.display.set_caption("Wifi Optimisation Algorithm")
        display_win = pygame.display.set_mode([200, 200])
        win = pygame.Surface((100, 100))

        WHITE = (200, 200, 200)
        GREY = (50, 50, 50)
        BLACK = (0, 0, 0)
        RED = (200, 0, 0)
        GREEN = (0, 255, 0)
        TAN = (240, 171, 15)
        YELLOW = (255, 255, 0)

        class Unit(pygame.sprite.Sprite):
            def __init__(self, x: int, y: int, colour=YELLOW, size=5):
                pygame.sprite.Sprite.__init__(self)
                self.colour = colour
                self.image = pygame.Surface((size, size), pygame.SRCALPHA)
                self.rect = self.image.get_rect()
                self.rect.center = (x, y)
                self.size = size
                self.seen = False
                pygame.draw.circle(
                    self.image, colour, (self.size // 2, self.size // 2), self.size // 2
                )

        win.fill(BLACK)

        user_sprites = pygame.sprite.Group()
        for user_location in users:
            user_sprites.add(Unit(*user_location, GREEN))
        user_sprites.update()
        user_sprites.draw(win)
        user_sprites.draw(win)

        router_sprite = pygame.sprite.GroupSingle()
        router = Unit(0, 0)
        router_sprite.add(router)
        router.rect.x = router_x
        router.rect.y = router_y
        router_sprite.draw(win)

        for wall in walls:
            pygame.draw.line(win, TAN, *wall)

        for user in users:
            for wall in walls:
                router_user = [(round(router_x), round(router_y)), user]
                pygame.draw.line(win, RED, *router_user)

        scaled_win = pygame.transform.smoothscale(win, display_win.get_size())
        display_win.blit(scaled_win, (0, 0))
        pygame.display.flip()

        pygame.image.save(
            display_win, "./examples/wifi_optimisation_screenshots/plan.png"
        )
        pygame.quit()

    def population_size(self):
        return 100

    def replacement_method(self) -> REPLACEMENT_METHOD:
        return REPLACEMENT_METHOD.WEAK_PARENT


if __name__ == "__main__":
    genetic_algorithm = WifiOptimisationGeneticAlgorithm()
    genetic_algorithm.run()

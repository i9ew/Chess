from functions import *


class HUDobjects:
    def __init__(self, objects=[]):
        self.objects = objects

    def draw(self, sc):
        for obj in self.objects:
            obj.draw(sc)

    def calculate_corners(self, corner, sqare_size, isreversed):
        for obj in self.objects:
            obj.calculate_corner(corner, sqare_size, isreversed)

    def clear(self):
        self.objects = []


class HUDobject:
    def __init__(self, group):
        group.objects.append(self)

    def draw(self, sc):
        pass

    def calculate_corner(self, corner, sqare_size, isreversed):
        pass


class CircleInSqare(HUDobject):
    def __init__(self, hud_group, color, alpha, placement, radius):
        if hud_group is not None:
            super().__init__(hud_group)
        self.color = color
        self.alpha = alpha
        self.placement = placement
        self.radius = radius
        self.corner = [0, 0]

    def calculate_corner(self, corner, sqare_size, isreversed):
        indexes = coards_to_indexes(self.placement)
        self.corner = [sqare_size * indexes[0],
                       sqare_size * indexes[1]]
        if isreversed:
            self.corner = [7 * sqare_size - self.corner[0], 7 * sqare_size - self.corner[1]]

        self.corner = [self.corner[0] + corner[0] + (sqare_size - self.radius * 2) // 2,
                       self.corner[1] + corner[1] + (sqare_size - self.radius * 2) // 2]

    def draw(self, sc):
        sur = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(sur, (*self.color.rgb, self.alpha), (self.radius, self.radius), self.radius)
        sc.blit(sur, self.corner)


class TrianglesInSqare(HUDobject):
    def __init__(self, hud_group, color, alpha, placement, size):
        if hud_group is not None:
            super().__init__(hud_group)
        self.color = color
        self.alpha = alpha
        self.placement = placement
        self.size = size
        self.corner = [0, 0]
        self.sqare_size = 0

    def calculate_corner(self, corner, sqare_size, isreversed):
        self.sqare_size = sqare_size
        indexes = coards_to_indexes(self.placement)
        self.corner = [sqare_size * indexes[0],
                       sqare_size * indexes[1]]
        if isreversed:
            self.corner = [7 * sqare_size - self.corner[0], 7 * sqare_size - self.corner[1]]

        self.corner = [self.corner[0] + corner[0],
                       self.corner[1] + corner[1]]

    def draw(self, sc):
        sur = pygame.Surface((self.sqare_size, self.sqare_size), pygame.SRCALPHA)
        tr1 = [[0, 0], [0, self.size],
               [self.size, 0]]
        tr2 = [[self.sqare_size, self.sqare_size], [self.sqare_size, self.sqare_size - self.size],
               [self.sqare_size - self.size, self.sqare_size]]
        tr3 = [[self.sqare_size, 0], [self.sqare_size, self.size],
               [self.sqare_size - self.size, 0]]
        tr4 = [[0, self.sqare_size], [0, self.sqare_size - self.size],
               [self.size, self.sqare_size]]
        pygame.draw.polygon(sur, (*self.color.rgb, self.alpha),
                            tr1)
        pygame.draw.polygon(sur, (*self.color.rgb, self.alpha),
                            tr2)
        pygame.draw.polygon(sur, (*self.color.rgb, self.alpha),
                            tr3)
        pygame.draw.polygon(sur, (*self.color.rgb, self.alpha),
                            tr4)
        sc.blit(sur, self.corner)

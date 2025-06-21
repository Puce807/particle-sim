import math

def compute_gravity(p1, p2, G):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.hypot(dx, dy)

    if distance == 0:
        return 0

    force = G * p1.mass * p2.mass / distance**2

    rx = dx / distance
    ry = dy / distance

    fx = force * rx
    fy = force * ry

    p1.fx += fx
    p1.fy += fy
    p2.fx -= fx
    p2.fy -= fy

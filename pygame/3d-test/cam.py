from math import radians
from ursina import *


class player_cam(Entity):
    def __init__(self, target, limits, offset = (0, 10, -25), smoothness = 1, lead_distance = 0.35, lead_smoothness = 1, look_smoothness = 6, vertical_look_scale = 0.35, look_height = 2, look_tilt = 5, edge_distance = 5, edge_shift = 8, edge_smoothness = 2.5):
        super().__init__()

        self.target = target
        self.limits = limits
        self.offset = Vec3(*offset)
        self.smoothness = smoothness
        self.lead_distance = lead_distance
        self.lead_smoothness = lead_smoothness

        # How slowly the camera turns towards the player, so it slides
        # sideways instead of snapping its rotation
        self.look_smoothness = look_smoothness

        # How much of the player's height the camera reacts to when aiming.
        # 0 ignores it completely, 1 tilts fully, 0.35 tilts slightly
        self.vertical_look_scale = vertical_look_scale
        self.look_height = look_height

        # Constant extra tilt in degrees, applied to the camera's aim direction
        # so it never changes no matter how the rig is smoothed.
        # Positive values tilt the camera down toward the ground.
        self.look_tilt = look_tilt

        # Edge behaviour: over the last edge_distance units, slide the camera
        # on that axis by up to edge_shift to keep the terrain in view
        self.edge_distance = edge_distance
        self.edge_shift = edge_shift
        self.edge_smoothness = edge_smoothness

        self.last_target_position = target.world_position
        self.lead = Vec3.zero
        self.edge_offset = Vec3.zero
        self.look_point = self.get_look_position()

        self.cam_follow = True

        camera.parent = self
        self.position = target.world_position + self.offset
        self.look_at(self.look_point)
        camera.look_in_direction(self.get_tilted_direction())

    def input(self, key):
        if key == "right mouse down":
            self.cam_follow = not self.cam_follow

    def get_tilted_direction(self):
        # Direction the camera should really look at: the rig's own forward
        # rotated down by look_tilt degrees, in world space. Working with the
        # vector instead of rotation_x keeps the tilt independent of the rig
        # rotation, so it stays constant while the camera tracks.
        angle = radians(self.look_tilt)
        forward = self.forward
        up = self.up

        # forward and up are orthonormal, so tilting forward toward -up by
        # angle gives a direction that stays normalized without renormalizing
        return forward * cos(angle) - up * sin(angle)

    def get_edge_offset(self):
        # 0 when far from the border, 1 when on the very edge, per axis
        position = self.target.world_position

        near_x = (self.limits.half_x - abs(position.x)) / self.edge_distance
        near_z = (self.limits.half_z - abs(position.z)) / self.edge_distance

        factor_x = clamp(1 - near_x, 0, 1)
        factor_z = clamp(1 - near_z, 0, 1)

        # Push the camera back toward the player on whichever axis is running out
        shift_x = -position.x / self.limits.half_x * factor_x * self.edge_shift
        shift_z = -position.z / self.limits.half_z * factor_z * self.edge_shift

        desired = Vec3(shift_x, 0, shift_z)
        return lerp(self.edge_offset, desired, time.dt * self.edge_smoothness)

    def get_look_position(self):
        # Where the camera aims, at the player's position but with its height
        # pulled toward the camera's own height so jumps barely tilt the view
        player = self.target.world_position

        aimed_height = self.offset.y + (player.y + self.look_height - self.offset.y) * self.vertical_look_scale
        return Vec3(player.x, aimed_height, player.z) + self.lead

    def update(self):
        # The camera only tracks the player on X and Z, its height stays fixed
        target_position = Vec3(self.target.world_position.x, self.offset.y, self.target.world_position.z)

        # Direction the player is moving, in world space and horizontal only
        velocity = (self.target.world_position - self.last_target_position) / time.dt
        self.last_target_position = self.target.world_position

        horizontal_velocity = Vec3(velocity.x, 0, velocity.z)
        if horizontal_velocity.length() > 0.01:
            self.lead = lerp(self.lead, horizontal_velocity.normalized() * self.lead_distance, time.dt * self.lead_smoothness)
        else:
            self.lead = lerp(self.lead, Vec3.zero, time.dt * self.lead_smoothness)

        self.edge_offset = self.get_edge_offset()

        if self.cam_follow:
            desired_position = target_position + Vec3(self.offset.x, 0, self.offset.z) + self.lead + self.edge_offset
        else:
            desired_position = Vec3(0, 10, -25)

        self.position = lerp(self.position, desired_position, time.dt * self.smoothness)

        # Keep looking at the player, but only tilt slightly toward its height
        self.look_point = lerp(self.look_point, self.get_look_position(), time.dt * self.look_smoothness)
        self.look_at(self.look_point)

        # Constant tilt on top of the aim, independent of the smoothing above
        camera.look_in_direction(self.get_tilted_direction())

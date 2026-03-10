from asyncio.windows_events import INFINITE

from Gutter import Gutter

class PIDController:
    def __init__(self, gutter:Gutter, kp, ki, kd):
        self.gutter = gutter
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.I = 0
        self.prev_e = INFINITE
        self.prev_u = 0
    def __call__(self, cur_ball_pos, desired_ball_pos, dt):
        if dt == 0: return
        e = desired_ball_pos - cur_ball_pos
        if abs(e) < 0.01 and abs(e - self.prev_e) < 0.01*dt:
            self.prev_e = e
            self.prev_u = 0
            self.gutter.set_angle(0)
            return
        if self.prev_e == INFINITE:
            self.prev_e = e
        P = e
        self.I += e * dt
        D = (e-self.prev_e) / dt
        self.prev_e = e
        max_ang_change = self.gutter.max_ang_vel * dt
        u = self.kp * P + self.ki * self.I + self.kd * D
        if abs(u - self.prev_u) > max_ang_change:
            if u > self.prev_u:
                u = self.prev_u + max_ang_change
            else:
                u = self.prev_u - max_ang_change
        self.prev_u = u
        self.gutter.set_angle(-u)
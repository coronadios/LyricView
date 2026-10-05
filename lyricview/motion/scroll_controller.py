"""Auto-scroll controller with damping for LyricView.

Produces a smooth, interruptible interpolated position that chases a target
position with configurable stiffness and damping. Designed to be driven from
an engine tick with a delta time.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScrollController:
    position: float = 0.0
    velocity: float = 0.0
    stiffness: float = 200.0
    damping: float = 20.0

    def set_immediate(self, pos: float) -> None:
        self.position = float(pos)
        self.velocity = 0.0

    def step(self, target: float, dt: float) -> float:
        """Advance the controller by dt seconds towards target and return new position."""
        if dt <= 0:
            return self.position

        # spring-damper differential approximation (semi-implicit Euler)
        # a = -stiffness * (x - target) - damping * v
        x = self.position
        v = self.velocity
        a = -self.stiffness * (x - target) - self.damping * v

        # integrate velocity and position
        v_new = v + a * dt
        x_new = x + v_new * dt

        self.position = x_new
        self.velocity = v_new
        return self.position

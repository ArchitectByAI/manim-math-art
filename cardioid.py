from manim import *
import numpy as np

# Set 9:16 vertical ratio
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920

class Epicycloid(Scene):
    def construct(self):
        # ------------------- SAFE ZONE SETUP -------------------
        # Define safe margins (top & bottom)
        top_margin = 1.5
        bottom_margin = 1.5
        content_height = config.frame_height - top_margin - bottom_margin

        # Center of animation
        center_x = 0
        center_y = 0

        # ------------------- TEXT ELEMENTS (TOP & BOTTOM) -------------------
        # Header (Top)
        title = Text("CARDIOID ENVELOPE", font_size=36, color=YELLOW, weight=BOLD)
        subtitle = Text("120 Circles through Point A", font_size=24, color=WHITE)
        header_group = VGroup(title, subtitle).arrange(DOWN, aligned_edge=LEFT)
        header_group.to_edge(UP, buff=0.7)

        # Formula (Bottom)
        formula = Text(
            "x = 2cos(t) - cos(2t)\ny = 2sin(t) - sin(2t)",
            font_size=20,
            color=RED,
        ).to_edge(DOWN, buff=0.7)

        # Watermark (Bottom Right)
        watermark = Text("@architectbyai", font_size=16, color=GRAY, weight=BOLD)
        watermark.to_corner(DR, buff=0.5)

        # Add all text first
        self.add(header_group, formula, watermark)

        # ------------------- ANIMATION AREA (Centered) -------------------
        # Shift geometry to center in middle zone
        shift_y = 0  # keep it centered vertically

        base_radius = 1.1
        base_circle = Circle(radius=base_radius, color=BLUE_E, stroke_width=3)
        base_circle.shift(UP * shift_y)

        # Fixed point A
        A_pos = np.array([base_radius, 0, 0]) + UP * shift_y
        dot_A = Dot(A_pos, color=RED, radius=0.08)
        label_A = Text("A", font_size=18, color=RED).next_to(dot_A, UP)

        # Draw base circle and point
        self.play(Create(base_circle), FadeIn(dot_A), Write(label_A), run_time=1)

        # Moving center
        moving_center = Dot(color=YELLOW, radius=0.07)
        self.add(moving_center)

        num_circles = 100
        colors = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], num_circles)

        for i in range(num_circles):
            theta = (i / num_circles) * TAU
            new_pos = np.array([
                base_radius * np.cos(theta),
                base_radius * np.sin(theta),
                0
            ]) + UP * shift_y

            radius = np.linalg.norm(new_pos - A_pos)

            circle = Circle(
                radius=radius,
                color=colors[i],
                stroke_width=1.5,
                stroke_opacity=0.8
            ).move_to(new_pos)

            self.play(
                moving_center.animate.move_to(new_pos),
                Create(circle),
                run_time=0.05,
                rate_func=linear
            )

        # Remove moving dot
        self.remove(moving_center)

        # ------------------- FINAL CARDIOID -------------------
        t = np.linspace(0, TAU, 400)
        cardioid_points = [
            np.array([
                base_radius * (2 * np.cos(phi) - np.cos(2 * phi)),
                base_radius * (2 * np.sin(phi) - np.sin(2 * phi)),
                0
            ]) + UP * shift_y
            for phi in t
        ]

        cardioid = VMobject(color=RED, stroke_width=5)
        cardioid.set_points_as_corners(cardioid_points)

        self.play(Create(cardioid), run_time=1.5)
        self.wait(2)

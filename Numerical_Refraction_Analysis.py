from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button

BASE_DIR = Path(__file__).resolve().parent
FIGURES_DIR = BASE_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

MATERIALS = {
    "Air": 1.000,
    "Water": 1.333,
    "Glass": 1.500,
    "Diamond": 2.417,
    "Custom": None
}

def snell_angle(n1, n2, theta1):
    value = (n1 / n2) * np.sin(np.radians(theta1))
    if abs(value) > 1:
        return None
    return np.degrees(np.arcsin(value))

def critical_angle(n1, n2):
    if n1 <= n2:
        return None
    return np.degrees(np.arcsin(n2 / n1))

def snell_residual(n1, n2, theta1, theta2):
    return (
        n1 * np.sin(np.radians(theta1))
        - n2 * np.sin(np.radians(theta2))
    )

def save_figure(figure, filename):
    path = FIGURES_DIR / filename
    figure.savefig(
        path,
        dpi=300,
        bbox_inches="tight"
    )
    print(f"Saved: {path}")

def draw_angle(ax, theta, radius, side):
    if side == "incident":
        angles = np.linspace(
            np.radians(90),
            np.radians(90 + theta),
            100
        )
    else:
        angles = np.linspace(
            np.radians(270),
            np.radians(270 + theta),
            100
        )

    ax.plot(
        radius * np.cos(angles),
        radius * np.sin(angles),
        linewidth=2
    )

def create_angle_sweep():
    angles = np.linspace(0, 89.9, 500)

    figure, ax = plt.subplots(figsize=(10, 7))

    for name in ["Water", "Glass", "Diamond"]:
        n2 = MATERIALS[name]

        transmitted = np.degrees(
            np.arcsin(
                np.sin(np.radians(angles)) / n2
            )
        )

        ax.plot(
            angles,
            transmitted,
            linewidth=2.5,
            label=name
        )

    ax.plot(
        angles,
        angles,
        linestyle="--",
        linewidth=1.5,
        label="No bending"
    )

    ax.set_title(
        "Snell's Law: Incident Angle vs Refracted Angle",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel(
        "Incident angle θᵢ (degrees)"
    )

    ax.set_ylabel(
        "Refracted angle θₜ (degrees)"
    )

    ax.set_xlim(0, 90)
    ax.set_ylim(0, 90)
    ax.grid(alpha=0.25)
    ax.legend()

    figure.tight_layout()

    return figure

def create_tir():
    n1 = MATERIALS["Glass"]
    n2 = MATERIALS["Air"]

    theta = 50
    critical = critical_angle(n1, n2)

    figure, ax = plt.subplots(figsize=(9, 8))

    ax.axhline(0, linewidth=2)
    ax.axvline(
        0,
        linestyle="--",
        linewidth=1.5
    )

    length = 3

    incident_x = np.linspace(-length, 0, 200)
    incident_y = (
        -np.tan(np.radians(theta))
        * incident_x
    )

    reflected_x = np.linspace(0, length, 200)
    reflected_y = (
        np.tan(np.radians(theta))
        * reflected_x
    )

    ax.plot(
        incident_x,
        incident_y,
        linewidth=4,
        label="Incident ray"
    )

    ax.plot(
        reflected_x,
        reflected_y,
        linewidth=4,
        label="Reflected ray"
    )

    ax.text(
        -2.75,
        2.55,
        f"Glass → Air\n"
        f"θᵢ = {theta:.1f}°\n"
        f"θc = {critical:.2f}°",
        fontsize=13,
        verticalalignment="top"
    )

    ax.set_title(
        "Total Internal Reflection",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Horizontal position")
    ax.set_ylabel("Vertical position")

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_aspect("equal")

    ax.grid(alpha=0.2)
    ax.legend()

    figure.tight_layout()

    return figure

def create_material_comparison():
    theta1 = 45

    names = [
        "Air",
        "Water",
        "Glass",
        "Diamond"
    ]

    values = []

    for name in names:
        theta2 = snell_angle(
            1.0,
            MATERIALS[name],
            theta1
        )

        values.append(theta2)

    figure, ax = plt.subplots(figsize=(10, 7))

    bars = ax.bar(
        names,
        values
    )

    ax.set_title(
        "Material Dependence of Refraction",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Medium")

    ax.set_ylabel(
        "Refracted angle θₜ (degrees)"
    )

    ax.grid(
        axis="y",
        alpha=0.25
    )

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.2f}°",
            ha="center"
        )

    figure.tight_layout()

    return figure

def selected_n2():
    material = material_buttons.value_selected

    if material == "Custom":
        return custom_slider.val

    return MATERIALS[material]

def update(_=None):
    theta1 = angle_slider.val
    n1 = 1.0

    material = material_buttons.value_selected
    n2 = selected_n2()

    theta2 = snell_angle(
        n1,
        n2,
        theta1
    )

    critical = critical_angle(
        n1,
        n2
    )

    sim_ax.clear()
    graph_ax.clear()
    info_ax.clear()

    custom_ax.set_visible(
        material == "Custom"
    )

    sim_ax.set_xlim(-3, 3)
    sim_ax.set_ylim(-3, 3)
    sim_ax.set_aspect("equal")

    sim_ax.axhline(
        0,
        linewidth=2
    )

    sim_ax.axvline(
        0,
        linestyle="--",
        linewidth=1.5
    )

    sim_ax.text(
        -2.85,
        2.65,
        f"Medium 1: Air (n₁ = {n1:.3f})",
        fontsize=11
    )

    sim_ax.text(
        -2.85,
        -2.65,
        f"Medium 2: {material} (n₂ = {n2:.3f})",
        fontsize=11
    )

    length = 2.7

    incident_x = (
        -length
        * np.sin(np.radians(theta1))
    )

    incident_y = (
        length
        * np.cos(np.radians(theta1))
    )

    sim_ax.plot(
        [incident_x, 0],
        [incident_y, 0],
        linewidth=3,
        label="Incident"
    )

    reflected_x = (
        length
        * np.sin(np.radians(theta1))
    )

    reflected_y = (
        length
        * np.cos(np.radians(theta1))
    )

    sim_ax.plot(
        [0, reflected_x],
        [0, reflected_y],
        linestyle="--",
        linewidth=2.5,
        label="Reflected"
    )

    draw_angle(
        sim_ax,
        theta1,
        0.8,
        "incident"
    )

    sim_ax.text(
        -1.3,
        0.55,
        f"θᵢ = {theta1:.1f}°",
        fontsize=11
    )

    if theta2 is not None:
        transmitted_x = (
            length
            * np.sin(np.radians(theta2))
        )

        transmitted_y = (
            -length
            * np.cos(np.radians(theta2))
        )

        sim_ax.plot(
            [0, transmitted_x],
            [0, transmitted_y],
            linewidth=3,
            label="Refracted"
        )

        draw_angle(
            sim_ax,
            theta2,
            0.8,
            "refracted"
        )

        sim_ax.text(
            0.35,
            -0.75,
            f"θₜ = {theta2:.1f}°",
            fontsize=11
        )

        state = "Transmission"

    else:
        state = "Total Internal Reflection"

    sim_ax.set_title(
        "Numerical Refraction Analysis",
        fontsize=15,
        fontweight="bold"
    )

    sim_ax.set_xlabel(
        "Horizontal position"
    )

    sim_ax.set_ylabel(
        "Vertical position"
    )

    sim_ax.grid(alpha=0.2)
    sim_ax.legend()

    angles = np.linspace(
        0,
        89.9,
        500
    )

    values = (
        np.sin(np.radians(angles))
        * n1
        / n2
    )

    transmitted = np.full_like(
        angles,
        np.nan
    )

    valid = np.abs(values) <= 1

    transmitted[valid] = np.degrees(
        np.arcsin(values[valid])
    )

    graph_ax.plot(
        angles,
        transmitted,
        linewidth=2.5
    )

    graph_ax.plot(
        angles,
        angles,
        linestyle="--",
        linewidth=1.2
    )

    if theta2 is not None:
        graph_ax.scatter(
            theta1,
            theta2,
            s=60
        )

    if critical is not None:
        graph_ax.axvline(
            critical,
            linestyle=":",
            linewidth=1.5
        )

        graph_ax.text(
            critical + 1,
            5,
            f"θc = {critical:.2f}°",
            fontsize=9
        )

    graph_ax.set_xlim(0, 90)
    graph_ax.set_ylim(0, 90)

    graph_ax.set_xlabel(
        "θᵢ (degrees)"
    )

    graph_ax.set_ylabel(
        "θₜ (degrees)"
    )

    graph_ax.set_title(
        "Angular Response",
        fontweight="bold"
    )

    graph_ax.grid(alpha=0.2)

    info_ax.axis("off")

    residual = None

    if theta2 is not None:
        residual = snell_residual(
            n1,
            n2,
            theta1,
            theta2
        )

    lines = [
        f"State: {state}",
        f"Incident angle: {theta1:.2f}°",
        f"n₁ = {n1:.3f}",
        f"n₂ = {n2:.3f}"
    ]

    if theta2 is not None:
        lines.extend([
            f"Refracted angle: {theta2:.2f}°",
            f"Snell residual: {residual:.3e}"
        ])
    else:
        lines.append(
            "No real transmitted angle"
        )

    if critical is not None:
        lines.append(
            f"Critical angle: {critical:.2f}°"
        )

    info_ax.text(
        0.02,
        0.95,
        "\n".join(lines),
        verticalalignment="top",
        fontsize=11
    )

    fig.canvas.draw_idle()

def reset():
    material_buttons.set_active(2)
    angle_slider.reset()
    custom_slider.reset()

def save_hero():
    save_figure(
        fig,
        "hero.png"
    )

def show_sweep(_=None):
    figure = create_angle_sweep()

    save_figure(
        figure,
        "angle_sweep.png"
    )

    figure.show()

def show_tir(_=None):
    figure = create_tir()

    save_figure(
        figure,
        "total_internal_reflection.png"
    )

    figure.show()

def show_materials(_=None):
    figure = create_material_comparison()

    save_figure(
        figure,
        "material_comparison.png"
    )

    figure.show()

fig = plt.figure(
    figsize=(14, 8)
)

sim_ax = fig.add_axes(
    [0.05, 0.22, 0.52, 0.68]
)

graph_ax = fig.add_axes(
    [0.63, 0.55, 0.32, 0.35]
)

info_ax = fig.add_axes(
    [0.63, 0.22, 0.32, 0.24]
)

angle_ax = fig.add_axes(
    [0.10, 0.10, 0.35, 0.035]
)

custom_ax = fig.add_axes(
    [0.63, 0.10, 0.25, 0.035]
)

material_ax = fig.add_axes(
    [0.63, 0.02, 0.17, 0.075]
)

reset_ax = fig.add_axes(
    [0.82, 0.07, 0.12, 0.04]
)

hero_ax = fig.add_axes(
    [0.82, 0.02, 0.12, 0.04]
)

sweep_ax = fig.add_axes(
    [0.40, 0.02, 0.12, 0.04]
)

tir_ax = fig.add_axes(
    [0.26, 0.02, 0.12, 0.04]
)

material_fig_ax = fig.add_axes(
    [0.12, 0.02, 0.12, 0.04]
)

angle_slider = Slider(
    angle_ax,
    "θᵢ",
    0,
    89,
    valinit=30,
    valstep=0.1
)

custom_slider = Slider(
    custom_ax,
    "n₂",
    1.01,
    3.0,
    valinit=1.5,
    valstep=0.001
)

material_buttons = RadioButtons(
    material_ax,
    list(MATERIALS.keys()),
    active=2
)

reset_button = Button(
    reset_ax,
    "Reset"
)

hero_button = Button(
    hero_ax,
    "Save Hero"
)

sweep_button = Button(
    sweep_ax,
    "Sweep"
)

tir_button = Button(
    tir_ax,
    "TIR"
)

material_fig_button = Button(
    material_fig_ax,
    "Materials"
)

angle_slider.on_changed(update)
custom_slider.on_changed(update)
material_buttons.on_clicked(update)

reset_button.on_clicked(reset)
hero_button.on_clicked(save_hero)
sweep_button.on_clicked(show_sweep)
tir_button.on_clicked(show_tir)
material_fig_button.on_clicked(show_materials)

update()

plt.show()
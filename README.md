# Numerical Refraction Analysis
A computational investigation of optical refraction using Snell's law, numerical modeling, and quantitative visualization.

<img width="1280" height="664" alt="hero" src="https://github.com/user-attachments/assets/22076823-a355-4983-bbe7-ba0494579b23" />

# Research Perspective
Refraction is usually introduced as a geometric-optics problem: given two refractive indices and an incident angle, determine the direction of the transmitted ray.

This project treats the same relationship as a computational experiment.

Rather than evaluating Snell's law for a single configuration, the analysis explores how the refracted angle changes across a range of incident angles and material indices, while identifying the transition from ordinary transmission to total internal reflection.

The central model is

[
n_1\sin\theta_i=n_2\sin\theta_t
]

with all angles measured relative to the surface normal.

For (n_1>n_2), the critical angle is

[
\theta_c=\sin^{-1}\left(\frac{n_2}{n_1}\right)
]

and transmission ceases when

[
\theta_i>\theta_c.
]

# Computational Method
The analysis was implemented in Python using NumPy and Matplotlib.

The model performs the following numerical operations:

evaluates the transmitted angle from Snell's law;
detects physically invalid transmitted angles;
calculates the critical angle when (n_1>n_2);
computes the numerical residual

[
R=n_1\sin\theta_i-n_2\sin\theta_t
]

as a consistency check;

sweeps incident angle over (0^\circ)–(89.9^\circ);
compares the angular response of different optical media;
visualizes total internal reflection;
supports user-defined refractive indices.

The refractive-index values used in the model are representative constants rather than a full dispersive optical-material model. In practice, refractive index depends on variables such as wavelength and temperature; NIST provides wavelength- and temperature-dependent reference data for optical materials.

# Computational Results
01 — Angular Response
<img width="1280" height="664" alt="angle_sweep" src="https://github.com/user-attachments/assets/0ba4cc3b-de23-424f-8be7-13423400a2a6" />

The parameter sweep shows the nonlinear relationship between incident and refracted angles.

As the refractive index of the second medium increases, the transmitted ray remains closer to the normal for a given incident angle. The numerical curves therefore provide a direct computational view of the angular dependence predicted by Snell's law.

02 — Total Internal Reflection
<img width="1280" height="664" alt="total_internal_reflection" src="https://github.com/user-attachments/assets/0c459dc9-9b1b-4e82-9f51-b561c1bac138" />

For a glass–air interface, increasing the incident angle beyond the critical angle produces no real transmitted solution.

The simulation therefore transitions from refraction to total internal reflection, reproducing the physical condition

[
n_1>n_2,\qquad \theta_i>\theta_c.
]

This is the same critical-angle behavior described in standard optics treatments.

03 — Material Dependence
<img width="1280" height="664" alt="material_comparison" src="https://github.com/user-attachments/assets/9c60df96-f372-4bb8-9396-115b0f361fa4" />

At a fixed incident angle, changing the refractive index changes the transmitted angle.

The comparison illustrates the fundamental relationship between optical density and ray deflection rather than treating each material as an isolated example.

# Validation
A useful computational model should not only produce a visually plausible result; it should also provide a quantitative consistency check.

For every transmitted ray, the implementation evaluates

[
R=n_1\sin\theta_i-n_2\sin\theta_t.
]

A correctly evaluated solution should produce a residual numerically close to zero, subject to floating-point precision.

The model therefore combines visual validation through ray geometry with numerical validation through the Snell-law residual.

# Why This Matters
Snell's law is a compact equation, but its consequences extend into important optical systems.

The same principles underlying the analysis appear in optical fibers, waveguides, imaging systems, and other technologies that depend on controlled propagation and reflection of light.

The broader objective of this project was therefore not simply to reproduce a textbook equation, but to practice the workflow of computational physics:

physical law → mathematical model → numerical implementation → parameter study → visualization → validation.

# Reproducibility
# Requirements
Python 3
NumPy
Matplotlib

The interactive analysis provides:

incident-angle control;
material selection;
custom refractive index;
refraction visualization;
angular-response analysis;
total-internal-reflection analysis;
material comparison;
high-resolution figure export.

# References
E. Hecht, Optics, Pearson.
OpenStax, College Physics 2e, Section 25.4 — Total Internal Reflection.
National Institute of Standards and Technology (NIST), Index of Refraction of Liquid Water.
Optical Society educational resource, Snell's Law, Reflection, and Refraction.

# Author
Durodola Daniel

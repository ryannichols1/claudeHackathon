# Politician Tracker Dashboard - Design Analysis

## Project Overview

The **Politician Tracker Dashboard** (Project ID: `751727043870268196`) is a Stitch project comprising three primary screens:
1. **Irish Political Parties**
2. **Party Members Directory**
3. **Politician Tracker Dashboard**

The project employs a dark mode visual theme defined by the "VIBRANT" color variant and heavily utilizes custom typography to create an authoritative data visualization experience.

---

## Design System: "The Digital Panopticon"

The core creative north star of the project is described as an "authoritative, high-stakes editorial experience," breaking away from standard SaaS Dashboard templates. By employing intentional asymmetry and high contrast, the system aims to present itself as a premium "source of truth."

### 1. Typography

The system leverages a dual-font structure to balance strong editorial presentation with high-density data readability:
*   **Headlines & Display (Manrope):** A modern, geometric sans-serif used for impact. Large display sizes (e.g., `display-lg` at 3.5rem) give metrics a powerful presence.
*   **Body & Labels (Inter):** The reliable standard for complex UI. Its strong x-height makes small text sizes (e.g., `label-sm` at 0.6875rem) legible in nested data tables.

### 2. Core Color Palette

The environment is anchored in dark, void-like background shades, with neon accents serving functional interactive purposes:
*   **Surface (Base):** `#0e0e10`
*   **Primary (Electric Blue):** `#97a9ff` (Navigation, interactive states)
*   **Secondary (Neon Green):** `#2ff801` (Indicates positive status, e.g., "Promise Kept")
*   **Tertiary/Error (Bright Red):** `#ff7166` (Indicates negative status, e.g., "Broken Promise")

*Text Contrast:* Pure white text is avoided in favor of slightly muted tones like `on_surface` (`#f9f5f8`) to reduce eye strain, prioritizing read order hierarchy.

### 3. Key Design Rules & Components

#### The "No-Line" Rule
Standard 1px borders are strictly prohibited. The design achieves sectioning through background color shifts instead (e.g., using `surface_container_low` against a `surface` background).

#### Depth & Layering
Instead of traditional drop shadows, depth is conveyed through:
*   **Inset Layers:** Placing darker containers (`#000000`) inside lighter cards (`#1f1f22`).
*   **Glassmorphism:** Using frosted glass effects (`blur(12px)`) on contextual menus and navigation components.
*   **Gradients:** Employing a 135-degree linear gradient on high-impact Calls-To-Action (CTAs).

#### Chips & Badges
*   **Kept Actions:** Neon green text on a dark green container (`#106e00`).
*   **Broken Actions:** Bright red text on a dark red container (`#f5282b`).
*   Both use complete rounding for a pill-shaped badge aesthetic.

#### Input Fields
Minimalist fields without full borders. A solid background block is used, highlighted by a 2px Primary left-border when focused.

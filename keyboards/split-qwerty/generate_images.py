#!/usr/bin/env python3
"""
Generate split keyboard overlay images for RetroArch.
Recreates the iOS soft keyboard that was removed in commit ef9dc83041.

Generates both landscape and portrait versions.

Usage: python3 generate_images.py

Requires: PIL/Pillow (pip3 install Pillow)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# === Configuration ===

# Colors (RGBA)
PANEL_BG_COLOR = (30, 30, 30, 180)  # Semi-transparent dark gray
KEY_BG_COLOR = (80, 80, 80, 200)    # Gray key background
KEY_TEXT_COLOR = (255, 255, 255, 255)  # White text
KEY_BORDER_COLOR = (60, 60, 60, 255)   # Darker border

# Key styling
KEY_CORNER_RADIUS = 6
PANEL_CORNER_RADIUS = 12

# Key size multipliers
KEY_SIZE_STANDARD = 1
KEY_SIZE_WIDE = 2


def get_font(size):
    """Try to load a good font, fall back to default."""
    font_paths = [
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill, outline=None):
    """Draw a rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)


def draw_key(draw, x, y, width, height, label, font, small_font):
    """Draw a single key."""
    draw_rounded_rect(
        draw,
        (x, y, x + width, y + height),
        KEY_CORNER_RADIUS,
        KEY_BG_COLOR,
        KEY_BORDER_COLOR
    )
    use_font = small_font if len(label) > 3 else font
    bbox = draw.textbbox((0, 0), label, font=use_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x + (width - text_width) // 2
    text_y = y + (height - text_height) // 2
    draw.text((text_x, text_y), label, fill=KEY_TEXT_COLOR, font=use_font)


def draw_panel(draw, panel_x, panel_y, panel_width, panel_height,
               keys_layout, key_width, key_height, key_padding,
               key_spacing, row_spacing, font, small_font):
    """Draw a keyboard panel at the specified position."""
    draw_rounded_rect(
        draw,
        (panel_x, panel_y, panel_x + panel_width, panel_y + panel_height),
        PANEL_CORNER_RADIUS,
        PANEL_BG_COLOR
    )

    for row_idx, row in enumerate(keys_layout):
        y = panel_y + key_padding + row_idx * (key_height + row_spacing)
        x = panel_x + key_padding

        for key_info in row:
            if key_info is None:
                x += key_width + key_spacing
                continue

            if isinstance(key_info, tuple):
                label, size = key_info
            else:
                label, size = key_info, KEY_SIZE_STANDARD

            actual_width = key_width * size + key_spacing * (size - 1) if size > 1 else key_width
            draw_key(draw, x, y, actual_width, key_height, label, font, small_font)
            x += actual_width + key_spacing


def draw_toggle_button(draw, x, y, label, font, btn_width=70, btn_height=30):
    """Draw a small toggle button."""
    draw_rounded_rect(
        draw,
        (x - btn_width // 2, y - btn_height // 2,
         x + btn_width // 2, y + btn_height // 2),
        KEY_CORNER_RADIUS,
        KEY_BG_COLOR,
        KEY_BORDER_COLOR
    )
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text((x - text_width // 2, y - text_height // 2),
              label, fill=KEY_TEXT_COLOR, font=font)


# === Key Layouts ===

LEFT_PRIMARY = [
    ["1", "2", "3", "4", "5"],
    ["Q", "W", "E", "R", "T"],
    ["A", "S", "D", "F", "G"],
    ["Z", "X", "C", "V", "B"],
    [("Shift", KEY_SIZE_STANDARD), "fn", ("^", KEY_SIZE_STANDARD), ("Space", KEY_SIZE_WIDE)],
]

LEFT_FN = [
    ["ESC", None, None, None, None],
    ["F1", "F2", "F3", "F4", "F5"],
    ["-", "=", "/", "[", "]"],
    [";", "~", ":", "?", "!"],
    [("Shift", KEY_SIZE_STANDARD), "fn", ("^", KEY_SIZE_STANDARD), ("Space", KEY_SIZE_WIDE)],
]

RIGHT_PRIMARY = [
    ["6", "7", "8", "9", "0"],
    ["Y", "U", "I", "O", "P"],
    ["H", "J", "K", "L", "'"],
    ["N", "M", ",", ".", "<x"],
    [("Alt", KEY_SIZE_STANDARD), ("Tab", KEY_SIZE_STANDARD), ("Return", KEY_SIZE_WIDE), None],
]

RIGHT_FN = [
    ["F6", "F7", "F8", "F9", "F10"],
    ["PgUp", "Home", "Ins", "End", "PgDn"],
    ["F11", "^", None, None, "F12"],
    ["<", "v", ">", None, "Del"],
    [None, None, ("Return", KEY_SIZE_WIDE), None],
]


class OverlayConfig:
    """Configuration for generating an overlay."""
    def __init__(self, name, width, height, panel_width, panel_height,
                 margin_x, margin_y, font_size, font_size_small,
                 key_padding, key_spacing, row_spacing,
                 toggle_btn_y_norm, toggle_btn_width, toggle_btn_height):
        self.name = name
        self.width = width
        self.height = height
        self.panel_width = panel_width
        self.panel_height = panel_height
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.font_size = font_size
        self.font_size_small = font_size_small
        self.key_padding = key_padding
        self.key_spacing = key_spacing
        self.row_spacing = row_spacing
        self.toggle_btn_y_norm = toggle_btn_y_norm
        self.toggle_btn_width = toggle_btn_width
        self.toggle_btn_height = toggle_btn_height

        # Calculate key dimensions
        cols, rows = 5, 5
        usable_w = panel_width - 2 * key_padding - (cols - 1) * key_spacing
        usable_h = panel_height - 2 * key_padding - (rows - 1) * row_spacing
        self.key_width = usable_w // cols
        self.key_height = usable_h // rows

    @property
    def aspect_ratio(self):
        return self.width / self.height


# Landscape config (16:9)
# Original Swift keyboard spans ~30% to ~95% of screen height
# Panels should be flush with screen edges
LANDSCAPE = OverlayConfig(
    name="landscape",
    width=1920,
    height=1080,
    panel_width=440,
    panel_height=680,
    margin_x=10,
    margin_y=50,
    font_size=22,
    font_size_small=17,
    key_padding=12,
    key_spacing=10,
    row_spacing=12,
    toggle_btn_y_norm=0.27,
    toggle_btn_width=80,
    toggle_btn_height=35,
)

# Portrait config (9:16)
PORTRAIT = OverlayConfig(
    name="portrait",
    width=1080,
    height=1920,
    panel_width=520,
    panel_height=420,
    margin_x=10,
    margin_y=10,
    font_size=20,
    font_size_small=15,
    key_padding=10,
    key_spacing=8,
    row_spacing=10,
    toggle_btn_y_norm=0.755,
    toggle_btn_width=90,
    toggle_btn_height=40,
)


def create_overlay(config, left_keys, right_keys, filename):
    """Create an overlay image for the given configuration."""
    img = Image.new('RGBA', (config.width, config.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    font = get_font(config.font_size)
    small_font = get_font(config.font_size_small)

    # Panel positions
    left_panel_x = config.margin_x
    left_panel_y = config.height - config.panel_height - config.margin_y
    right_panel_x = config.width - config.panel_width - config.margin_x
    right_panel_y = config.height - config.panel_height - config.margin_y

    # Toggle buttons
    osk_btn_x = int(0.03 * config.width)
    osk_btn_y = int(config.toggle_btn_y_norm * config.height)
    draw_toggle_button(draw, osk_btn_x, osk_btn_y, "Joypad", small_font,
                       config.toggle_btn_width, config.toggle_btn_height)

    menu_btn_x = int(0.97 * config.width)
    menu_btn_y = int(config.toggle_btn_y_norm * config.height)
    draw_toggle_button(draw, menu_btn_x, menu_btn_y, "Menu", small_font,
                       config.toggle_btn_width, config.toggle_btn_height)

    # Draw panels
    draw_panel(draw, left_panel_x, left_panel_y,
               config.panel_width, config.panel_height,
               left_keys, config.key_width, config.key_height,
               config.key_padding, config.key_spacing, config.row_spacing,
               font, small_font)

    draw_panel(draw, right_panel_x, right_panel_y,
               config.panel_width, config.panel_height,
               right_keys, config.key_width, config.key_height,
               config.key_padding, config.key_spacing, config.row_spacing,
               font, small_font)

    img.save(filename, 'PNG')
    print(f"Created: {filename}")

    return config


def generate_cfg_descriptors(config, left_keys, right_keys, overlay_idx, fn_target, orientation_target):
    """Generate cfg descriptors for an overlay.

    Args:
        config: OverlayConfig for dimensions
        left_keys, right_keys: Key layout arrays
        overlay_idx: Overlay index (0-3)
        fn_target: Target overlay name for fn layer switching
        orientation_target: Target overlay name for orientation switching (auto-rotate)
    """
    lines = []
    desc_idx = 0

    # Toggle buttons
    osk_x = 0.03
    osk_y = config.toggle_btn_y_norm
    btn_w = config.toggle_btn_width / config.width / 2
    btn_h = config.toggle_btn_height / config.height / 2
    lines.append(f'overlay{overlay_idx}_desc{desc_idx} = "osk_toggle,{osk_x:.4f},{osk_y:.4f},rect,{btn_w:.4f},{btn_h:.4f}"')
    desc_idx += 1

    menu_x = 0.97
    menu_y = config.toggle_btn_y_norm
    lines.append(f'overlay{overlay_idx}_desc{desc_idx} = "menu_toggle,{menu_x:.4f},{menu_y:.4f},rect,{btn_w:.4f},{btn_h:.4f}"')
    desc_idx += 1

    # Key mappings
    key_codes = {
        "1": "retrok_num1", "2": "retrok_num2", "3": "retrok_num3", "4": "retrok_num4", "5": "retrok_num5",
        "6": "retrok_num6", "7": "retrok_num7", "8": "retrok_num8", "9": "retrok_num9", "0": "retrok_num0",
        "Q": "retrok_q", "W": "retrok_w", "E": "retrok_e", "R": "retrok_r", "T": "retrok_t",
        "Y": "retrok_y", "U": "retrok_u", "I": "retrok_i", "O": "retrok_o", "P": "retrok_p",
        "A": "retrok_a", "S": "retrok_s", "D": "retrok_d", "F": "retrok_f", "G": "retrok_g",
        "H": "retrok_h", "J": "retrok_j", "K": "retrok_k", "L": "retrok_l",
        "Z": "retrok_z", "X": "retrok_x", "C": "retrok_c", "V": "retrok_v", "B": "retrok_b",
        "N": "retrok_n", "M": "retrok_m",
        "'": "retrok_quote", ",": "retrok_comma", ".": "retrok_period", "<x": "retrok_backspace",
        "Shift": "retrok_lshift", "fn": "overlay_next", "^": "retrok_lctrl", "Space": "retrok_space",
        "Alt": "retrok_lalt", "Tab": "retrok_tab", "Return": "retrok_return",
        "ESC": "retrok_escape",
        "F1": "retrok_f1", "F2": "retrok_f2", "F3": "retrok_f3", "F4": "retrok_f4", "F5": "retrok_f5",
        "F6": "retrok_f6", "F7": "retrok_f7", "F8": "retrok_f8", "F9": "retrok_f9", "F10": "retrok_f10",
        "F11": "retrok_f11", "F12": "retrok_f12",
        "-": "retrok_minus", "=": "retrok_equals", "/": "retrok_slash",
        "[": "retrok_leftbracket", "]": "retrok_rightbracket",
        ";": "retrok_semicolon", "~": "retrok_backquote", ":": "retrok_colon",
        "?": "retrok_question", "!": "retrok_exclaim",
        "PgUp": "retrok_pageup", "Home": "retrok_home", "Ins": "retrok_insert",
        "End": "retrok_end", "PgDn": "retrok_pagedown",
        "<": "retrok_left", "v": "retrok_down", ">": "retrok_right",
        "Del": "retrok_delete",
    }
    # Note: "^" in arrow context means up arrow
    arrow_up_positions = []  # Track where up arrow should be

    key_w_norm = config.key_width / config.width / 2
    key_h_norm = config.key_height / config.height / 2
    wide_key_w_norm = (config.key_width * 2 + config.key_spacing) / config.width / 2

    def add_panel_keys(panel_x_start, panel_y_start, keys_layout, is_fn_layer=False):
        nonlocal desc_idx
        for row_idx, row in enumerate(keys_layout):
            col = 0
            for key_info in row:
                if key_info is None:
                    col += 1
                    continue

                if isinstance(key_info, tuple):
                    label, size = key_info
                else:
                    label, size = key_info, KEY_SIZE_STANDARD

                # Calculate center position
                key_x = panel_x_start + config.key_padding + col * (config.key_width + config.key_spacing)
                key_y = panel_y_start + config.key_padding + row_idx * (config.key_height + config.row_spacing)

                if size == KEY_SIZE_WIDE:
                    center_x = key_x + config.key_width + config.key_spacing / 2
                    w_norm = wide_key_w_norm
                else:
                    center_x = key_x + config.key_width / 2
                    w_norm = key_w_norm

                center_y = key_y + config.key_height / 2
                cx_norm = center_x / config.width
                cy_norm = center_y / config.height

                # Handle special case: "^" can mean Ctrl or Up arrow
                if label == "^" and is_fn_layer and row_idx >= 2:
                    code = "retrok_up"
                else:
                    code = key_codes.get(label, f"unknown_{label}")

                lines.append(f'overlay{overlay_idx}_desc{desc_idx} = "{code},{cx_norm:.4f},{cy_norm:.4f},rect,{w_norm:.4f},{key_h_norm:.4f}"')

                if code == "overlay_next":
                    lines.append(f'overlay{overlay_idx}_desc{desc_idx}_next_target = {fn_target}')

                desc_idx += 1
                col += size

    # Left panel
    left_panel_x = config.margin_x
    left_panel_y = config.height - config.panel_height - config.margin_y
    is_fn = "F1" in str(left_keys)
    add_panel_keys(left_panel_x, left_panel_y, left_keys, is_fn)

    # Right panel
    right_panel_x = config.width - config.panel_width - config.margin_x
    right_panel_y = config.height - config.panel_height - config.margin_y
    add_panel_keys(right_panel_x, right_panel_y, right_keys, is_fn)

    # Hidden button for auto-rotate orientation switching
    # This button is tiny and positioned off-screen, but RetroArch's auto_rotate
    # code searches all overlay_next buttons for one targeting the opposite orientation
    lines.append(f'overlay{overlay_idx}_desc{desc_idx} = "overlay_next,0.0010,0.0010,rect,0.0010,0.0010"')
    lines.append(f'overlay{overlay_idx}_desc{desc_idx}_next_target = {orientation_target}')
    desc_idx += 1

    return lines, desc_idx


def main():
    os.makedirs("img", exist_ok=True)

    # Generate images
    create_overlay(LANDSCAPE, LEFT_PRIMARY, RIGHT_PRIMARY, "img/landscape-primary.png")
    create_overlay(LANDSCAPE, LEFT_FN, RIGHT_FN, "img/landscape-fn.png")
    create_overlay(PORTRAIT, LEFT_PRIMARY, RIGHT_PRIMARY, "img/portrait-primary.png")
    create_overlay(PORTRAIT, LEFT_FN, RIGHT_FN, "img/portrait-fn.png")

    print("\nAll images generated!")

    # Generate cfg
    print("\n=== Generating split-qwerty.cfg ===")

    cfg_lines = [
        "# Split QWERTY Keyboard Overlay for RetroArch",
        "# Recreates the iOS soft keyboard removed in commit ef9dc83041",
        "#",
        "# Landscape and portrait versions with Fn layer toggle",
        "# osk_toggle button returns to joypad overlay",
        "# menu_toggle button opens RetroArch menu",
        "",
        "overlays = 4",
        "",
    ]

    # Each config: (OverlayConfig, name, fn_target, orientation_target, left_keys, right_keys, index)
    configs = [
        (LANDSCAPE, "landscape-primary", "landscape-fn", "portrait-primary", LEFT_PRIMARY, RIGHT_PRIMARY, 0),
        (LANDSCAPE, "landscape-fn", "landscape-primary", "portrait-fn", LEFT_FN, RIGHT_FN, 1),
        (PORTRAIT, "portrait-primary", "portrait-fn", "landscape-primary", LEFT_PRIMARY, RIGHT_PRIMARY, 2),
        (PORTRAIT, "portrait-fn", "portrait-primary", "landscape-fn", LEFT_FN, RIGHT_FN, 3),
    ]

    for config, name, fn_target, orientation_target, left_keys, right_keys, idx in configs:
        descs, count = generate_cfg_descriptors(config, left_keys, right_keys, idx, fn_target, orientation_target)

        cfg_lines.append(f"# {name.replace('-', ' ').title()}")
        cfg_lines.append(f"overlay{idx}_name = {name}")
        cfg_lines.append(f"overlay{idx}_normalized = true")
        cfg_lines.append(f"overlay{idx}_full_screen = true")
        cfg_lines.append(f"overlay{idx}_aspect_ratio = {config.aspect_ratio:.6f}")
        cfg_lines.append(f"overlay{idx}_auto_x_separation = true")
        cfg_lines.append(f"overlay{idx}_overlay = img/{name}.png")
        cfg_lines.append(f"overlay{idx}_descs = {count}")
        cfg_lines.append("")
        cfg_lines.extend(descs)
        cfg_lines.append("")

    with open("split-qwerty.cfg", "w") as f:
        f.write("\n".join(cfg_lines))

    print("Created: split-qwerty.cfg")
    print("\nDone! Overlay ready for use.")


if __name__ == "__main__":
    main()

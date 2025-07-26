# inkscape(in windows, it will be "inkscape.com") has to be in the path
$dpi = 30

# the action bulttons
inkscape "action_button.svg" --export-id="layer1" --export-filename="action_button_A.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "action_button.svg" --export-id="g17" --export-filename="action_button_B.png" --export-id-only --export-type=png --export-dpi=$dpi

# the circular icons
inkscape "circular_icon.svg" --export-id="layer1" --export-filename="circular_icon_retroarch.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "circular_icon.svg" --export-id="g6" --export-filename="circular_icon_fast_forward.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "circular_icon.svg" --export-id="g4" --export-filename="circular_icon_rotate.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "circular_icon.svg" --export-id="g13" --export-filename="circular_icon_joystick.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "circular_icon.svg" --export-id="g15" --export-filename="circular_icon_dpad_icon.png" --export-id-only --export-type=png --export-dpi=$dpi

# the d_buttons
inkscape "d_button_horizontal.svg" --export-id="layer1" --export-filename="d_button_horizontal_left.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "d_button_horizontal.svg" --export-id="g11" --export-filename="d_button_horizontal_right.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "d_button_vertical.svg" --export-id="layer1" --export-filename="d_button_vertical_up.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "d_button_vertical.svg" --export-id="g11" --export-filename="d_button_vertical_down.png" --export-id-only --export-type=png --export-dpi=$dpi

# the function buttons
inkscape "function_button.svg" --export-id="g25" --export-filename="function_button_start.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "function_button.svg" --export-id="g19" --export-filename="function_button_select.png" --export-id-only --export-type=png --export-dpi=$dpi

# the joystick
inkscape "joystick.svg" --export-id="layer1" --export-filename="joystick_outer_circle.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "joystick.svg" --export-id="layer2" --export-filename="joystick_stick.png" --export-id-only --export-type=png --export-dpi=$dpi

# secondary shoulder buttons
inkscape "secondary_shoulder_button.svg" --export-id="g17" --export-filename="secondary_shoulder_button_L2.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "secondary_shoulder_button.svg" --export-id="layer1" --export-filename="secondary_shoulder_button_R2.png" --export-id-only --export-type=png --export-dpi=$dpi

# shoulder buttons
inkscape "shoulder_button.svg" --export-id="layer1" --export-filename="shoulder_button_L.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "shoulder_button.svg" --export-id="g11" --export-filename="shoulder_button_R.png" --export-id-only --export-type=png --export-dpi=$dpi

# turbo buttons
inkscape "turbo.svg" --export-id="layer1" --export-filename="turbo_filled.png" --export-id-only --export-type=png --export-dpi=$dpi
inkscape "turbo.svg" --export-id="g19" --export-filename="turbo.png" --export-id-only --export-type=png --export-dpi=$dpi

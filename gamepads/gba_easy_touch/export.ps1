param (
    # dpi
    [Parameter()]
    [int]
    $dpi = 20
)

# function to verify whether a command is in the environment variables or not
function Find-Command {
    param(
        [Parameter(Mandatory = $true)]
        [string]
        $command
    )
    
    if ($null -ne (Get-Command $command -ErrorAction Ignore)) {
        Write-Host "`"$($command)`" was found in your Environment Variables" -ForegroundColor Green
    }
    else {
        Write-Host "`"$($command)`" was not found in you Environment Variables." -ForegroundColor Red
        $Script:something_missing = $true
    }
    
}

# inkscape(in windows, it will be "inkscape.com") has to be in the path
$something_missing = $false
$img_directory = "img"
$file = @('action_button_A.png', 'action_button_B.png', 'circular_icon_retroarch.png', 'circular_icon_fast_forward.png', 'circular_icon_rotate.png', 'circular_icon_joystick.png', 'circular_icon_dpad_icon.png', 'd_button_horizontal_left.png', 'd_button_horizontal_right.png', 'd_button_vertical_up.png', 'd_button_vertical_down.png', 'function_button_start.png', 'function_button_select.png', 'joystick_outer_circle.png', 'joystick_stick.png', 'secondary_shoulder_button_L2.png', 'secondary_shoulder_button_R2.png', 'shoulder_button_L.png', 'shoulder_button_R.png', 'turbo_filled.png', 'turbo.png')
$extra_commands = $("--export-id-only", "--export-type=png", "--export-dpi=$($dpi)")

# checking requirements
Find-Command "inkscape"
# Find-Command "magick"

# exit if something is missing and tell that to the user.
if($something_missing) {
    Write-Host "Add the missing command/executables to your environment variables to continue" -ForegroundColor Yellow
    exit
}

# export the icons
# the action bulttons
Write-Host "Exporting the action buttons"
inkscape "action_button.svg" --export-id="layer1" --export-filename="$($file[0])" @extra_commands *> $null
inkscape "action_button.svg" --export-id="g17" --export-filename="$($file[1])" @extra_commands *> $null

# the circular icons
Write-Host "Exporting the circular icons"
inkscape "circular_icon.svg" --export-id="layer1" --export-filename="$($file[2])" @extra_commands *> $null
inkscape "circular_icon.svg" --export-id="g6" --export-filename="$($file[3])" @extra_commands *> $null
inkscape "circular_icon.svg" --export-id="g4" --export-filename="$($file[4])" @extra_commands *> $null
inkscape "circular_icon.svg" --export-id="g13" --export-filename="$($file[5])png" @extra_commands *> $null
inkscape "circular_icon.svg" --export-id="g15" --export-filename="$($file[6])" @extra_commands *> $null

# the d_buttons
Write-Host "Exporting the d buttons"
inkscape "d_button_horizontal.svg" --export-id="layer1" --export-filename="$($file[7])" @extra_commands *> $null
inkscape "d_button_horizontal.svg" --export-id="g11" --export-filename="$($file[8])" @extra_commands *> $null
inkscape "d_button_vertical.svg" --export-id="layer1" --export-filename="$($file[9])" @extra_commands *> $null
inkscape "d_button_vertical.svg" --export-id="g11" --export-filename="$($file[10])" @extra_commands *> $null

# the function buttons
Write-Host "Exporting the function buttons"
inkscape "function_button.svg" --export-id="g25" --export-filename="$($file[11])" @extra_commands *> $null
inkscape "function_button.svg" --export-id="g19" --export-filename="$($file[12])" @extra_commands *> $null

# the joystick
Write-Host "Exporting the joystick"
inkscape "joystick.svg" --export-id="layer1" --export-filename="$($file[13])" @extra_commands *> $null
inkscape "joystick.svg" --export-id="layer2" --export-filename="$($file[14])" @extra_commands *> $null

# secondary shoulder buttons
Write-Host "Exporting the secondary shoulder buttons"
inkscape "secondary_shoulder_button.svg" --export-id="g17" --export-filename="$($file[15])" @extra_commands *> $null
inkscape "secondary_shoulder_button.svg" --export-id="layer1" --export-filename="$($file[16])" @extra_commands *> $null

# shoulder buttons
Write-Host "Exporting the shoulder buttons"
inkscape "shoulder_button.svg" --export-id="layer1" --export-filename="$($file[17])" @extra_commands *> $null
inkscape "shoulder_button.svg" --export-id="g11" --export-filename="$($file[18])" @extra_commands *> $null

# turbo buttons
Write-Host "Exporting the turbo buttons"
inkscape "turbo.svg" --export-id="layer1" --export-filename="$($file[19])" @extra_commands *> $null
inkscape "turbo.svg" --export-id="g19" --export-filename="$($file[20])" @extra_commands *> $null

# check whether the img folder exist or not
Write-Host "Checking whether the img folder exist or not"
$img_exist = Test-Path -LiteralPath $img_directory

# if the folder doesnt exit, create the folder
if($img_exist -eq $false){
    Write-Host "Creating the img folder"
    New-Item -ItemType Directory -Name $img_directory
}
else {
    Write-Host "The img folder exist"
}

# move the icons to the img folder
Write-Host "Moving the icons to the img directory"
$n = $file.Length
for ($i = 0; $i -lt $n; $i++) {
    Move-Item -Path $file[$i] -Destination $img_directory -Force
}


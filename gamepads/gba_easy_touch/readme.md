# Info

The `export.ps1` file uses `inkscape` command to produce the icons.

# Usage

Simply running the PowerShell file will start producng the icons. However, the PowerShell file takes an optional parameter:

1. `-dpi` : It is used to control the resolution. The icon size and resolution can be controlled with this parameter. This is used by Inkscape. The default value is **20**.

## Examples

```shell
pwsh export.ps1
```

```shell
pwsh export.ps1 -dpi 50
```

# `img` folder

After all image is produced, everything will be moved to the `img` folder. If the folder doesn't exist, it will be created. If it exist and there are icons in that folder, those icons will be replaced.

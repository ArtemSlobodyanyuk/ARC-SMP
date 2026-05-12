param(
  [string]$ShortcutName = "ARC Platform",
  [ValidateSet("Desktop","StartMenu")][string]$Location = "Desktop"
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$target = Join-Path $repoRoot "scripts\windows\run_arc.cmd"

if (-not (Test-Path $target)) {
  throw "Target not found: $target"
}

switch ($Location) {
  "Desktop" {
    $shortcutDir = [Environment]::GetFolderPath("Desktop")
  }
  "StartMenu" {
    $shortcutDir = [Environment]::GetFolderPath("Programs")
  }
}

$lnkPath = Join-Path $shortcutDir ("$ShortcutName.lnk")

$wsh = New-Object -ComObject WScript.Shell
$sc = $wsh.CreateShortcut($lnkPath)
$sc.TargetPath = $target
$sc.WorkingDirectory = $repoRoot
$sc.IconLocation = "$env:SystemRoot\System32\shell32.dll, 3"
$sc.Save()

Write-Host "Created shortcut: $lnkPath"

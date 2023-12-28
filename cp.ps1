param (
    [string]$s,
    [string]$d
)


$IsWindows = $env:OS -match "Windows_NT"
function Clear-Screen {
    if ($IsWindows) {
        Clear-Host
    } else {
        Clear
    }
}

function Logo {
    Clear-Screen
    Write-Host "   ___  _____   _____ _ __  " -ForegroundColor Cyan
    Write-Host "  / __|/ _ \ \ / / _ \ |_ \ " -ForegroundColor Cyan
    Write-Host "  \__ \  __/\ V /  __/ | | |" -ForegroundColor Cyan
    Write-Host "  |___/\___| \_/ \___|_| |_|" -ForegroundColor Cyan
    Write-Host "                            " -ForegroundColor Cyan
}
Logo

if (-not $s -or -not $d) {
    Write-Host "[+] Usage: .\move.ps1 -s 'D:\Source' -d 'F:\dest'"
    exit
}

$fileList = Get-ChildItem -Path $s -File

foreach ($file in $fileList) {
    $fileName = $file.BaseName -split '_'
    $fileDate = $fileName[0]

    $folderPath = Join-Path -Path $d -ChildPath $fileDate

    if (-not (Test-Path -Path $folderPath -PathType Container)) {
        Write-Host "[+] Creating folder: $folderPath"
        New-Item -Path $folderPath -ItemType Directory
    }

    $destinationPath = Join-Path -Path $folderPath -ChildPath $file.Name
	if (Test-Path -Path $destinationPath -PathType Leaf) {
        Write-Host "File $($file.Name) already exists in folder: $folderPath, skipping..."
        continue
    }

    try {
	$stream = [System.IO.File]::Open($file.FullName, 'Open', 'Read', 'None')
        $stream.Close()
        Write-Host "[+] Copying file $($file.Name) to folder: $folderPath"
        Copy-Item -Path $file.FullName -Destination $destinationPath -ErrorAction Stop
    } catch {
        Write-Host "[*] File $($file.Name) is in use, skipping..."
    }
}

Write-Host "[+] Done!..."

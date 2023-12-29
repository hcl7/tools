param (
    [string]$sn
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

if (-not $sn) {
    Write-Host "[+] Usage: .\ren.ps1 -sn 'D:\Source'"
    exit
}

$fileList = Get-ChildItem -Path $sn -File

foreach ($file in $fileList) {
    $fileNameComponents = $file.BaseName -split '_'

    if ($fileNameComponents.Count -lt 3) {
        Write-Host "[*] Invalid file name format for $($file.Name), skipping..."
        continue
    }

    $sourceDate = $fileNameComponents[0]
    $sourceTime = $fileNameComponents[1]
    $sourceIndex = $fileNameComponents[2]

    $sourceDateTimeString = "$sourceDate $sourceTime"
    $sourceDateTime = [DateTime]::ParseExact($sourceDateTimeString, 'yyyy.MM.dd HH.mm.ss', $null)

    $destinationDateTime = $sourceDateTime.AddHours(-1)

    $destinationDate = "x $($destinationDateTime.ToString('yyyy-MM-dd'))"
    $destinationIndex = [int]$sourceIndex

    $streamLabel = "STREAM $destinationIndex"

    $destinationExtension = $file.Extension
    $destinationName = "$destinationDate $sourceTime $($destinationDateTime.ToString('yyyy-MM-dd HH.mm.ss')) 01.00.00 0000000 $streamLabel$destinationExtension"
    $destinationPath = Join-Path -Path $sn -ChildPath "$destinationName"

    if (Test-Path -Path $destinationPath) {
        Write-Host "[-] Destination file $destinationName already exists, skipping..."
        continue
    }

    # Rename the file
    Write-Host "[+] Renaming file $($file.Name) to $destinationName"
    Rename-Item -Path $file.FullName -NewName "$destinationName" -ErrorAction SilentlyContinue
}

Write-Host "[+] Done!..."

param (
    [Parameter(Mandatory = $true)]
    [string] $DirectoryPath
)

function PrintTree($item, $indent)
{
    Write-Host ("{0}{1}" -f $indent, $item.Name)

    if ($item.PSIsContainer)
    {
        $childItems = Get-ChildItem -Path $item.FullName | Where-Object {
            $_.Name -notlike ".*" -and !$_.Attributes.HasFlag([IO.FileAttributes]::Hidden)
        }

        foreach ($childItem in $childItems)
        {
            PrintTree $childItem ($indent + "  ")
        }
    }
}

Write-Host "Generating file tree..."
try
{
    $rootItems = Get-ChildItem -Path $DirectoryPath | Where-Object {
        $_.Name -notlike ".*" -and !$_.Attributes.HasFlag([IO.FileAttributes]::Hidden)
    }

    foreach ($rootItem in $rootItems)
    {
        PrintTree $rootItem ""
    }

    Write-Host "File tree generation completed."
}
catch
{
    Write-Host "An error occurred during file tree generation: $_"
    $_.Exception.ToString() | Out-File -FilePath $ErrorLogFile -Append
}

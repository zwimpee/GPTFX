$ErrorActionPreference = "Stop"
$ErrorLogFile = Join-Path -Path $PSScriptRoot -ChildPath "logs/conda_cleanup.log"

Write-Host "Cleaning up Conda environments..."
try
{
    $environments = conda env list | Select-String -Pattern '^\S+' -AllMatches | ForEach-Object {
        $_.Matches.Value
    }

    foreach ($envName in $environments)
    {
        if ($envName -ne 'base')
        {
            try
            {
                conda env remove -n $envName -y
                Write-Host "Removed environment '$envName'"
            }
            catch
            {
                Write-Host "Failed to remove environment '$envName': $_"
                $_.Exception.ToString() | Out-File -FilePath $ErrorLogFile -Append
            }
        }
    }

    Write-Host "Conda environment cleanup completed."
}
catch
{
    Write-Host "An error occurred during Conda environment cleanup: $_"
    $_.Exception.ToString() | Out-File -FilePath $ErrorLogFile -Append
}

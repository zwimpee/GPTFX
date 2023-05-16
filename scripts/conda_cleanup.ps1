# Get a list of conda environments
$envs = conda env list | %{ $_.Split()[0] } | ?{ $_ }

# Loop through the environments
foreach ($env in $envs) {
    # Skip the base environment
    if ($env -eq 'base') {
        continue
    }
    # Remove the current environment
    conda env remove --name $env
}

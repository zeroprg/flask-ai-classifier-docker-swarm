# Ensure user is running Docker 19.03 or newer
$dockerVersion = (docker --version) -replace '[^\d.]'
if ([Version]$dockerVersion -lt [Version]"19.03") {
    Write-Output "You need Docker version 19.03 or newer"
    exit
}

# Enable experimental CLI features
$env:DOCKER_CLI_EXPERIMENTAL = "enabled"

# Install docker-buildx if not already installed
if (-not (docker buildx inspect default 2>$null)) {
    docker plugin install docker/cli-plugin/docker-buildx
}

# Create and bootstrap the builder
$builderName = "mybuilder"

docker buildx create --name $builderName --use
docker buildx inspect $builderName --bootstrap

Write-Output "Buildx preparation completed."

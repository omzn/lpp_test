#!/bin/bash

set -eo pipefail

echo "=============================================="
echo "Welcome to KIT Language Processing Programming"
echo "=============================================="

# Set the environment variables
DOCKER_IMAGE="ghcr.io/f0reacharr/lpp_test"
CONFIG_FILE="config.env"
CONFIG_BASE_DIR=${XDG_CONFIG_HOME:-$HOME/.config}
CONFIG_DIR="$CONFIG_BASE_DIR/lpp"
CONFIG_PATH="$CONFIG_DIR/$CONFIG_FILE"

should_check_update() {
    if [ ! -f "$CONFIG_PATH" ]; then
        return 0
    fi

    CONFIG_LAST_MODIFIED=$(stat -c %Y "$CONFIG_PATH")
    NOW=$(date +%s)

    DIFF=$((NOW - CONFIG_LAST_MODIFIED))
    if [ $DIFF -gt 86400 ]; then
        return 0
    fi

    return 1
}

debug_build_image() {
    docker buildx build -t "$DOCKER_IMAGE" "$DOCKER_IMAGE_ROOT"
}

pull_image() {
    OLD_IMAGE_ID=$(docker images --filter=reference=${DOCKER_IMAGE} --format "{{.ID}}")
    docker pull "$DOCKER_IMAGE"
    for ID in $OLD_IMAGE_ID; do
        echo Cleaning up old image $ID
        docker rmi $ID
    done
}

check_update() {
    echo "Checking for updates..."
    # If build root is set, build the image
    if [ -z $DOCKER_IMAGE_ROOT ]; then
        pull_image
    fi

    touch "$CONFIG_PATH"
}

# Ensure the config directory exists
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
fi

if [ ! -f "$CONFIG_PATH" ]; then
    touch "$CONFIG_PATH"
fi

source "$CONFIG_PATH"

if [ ! -z $DOCKER_IMAGE_ROOT ]; then
    debug_build_image
fi

if should_check_update; then
    check_update
fi

# Prepare bash history
DOCKER_HISTFILE="$CONFIG_DIR/bash_history"
touch "$DOCKER_HISTFILE"

# Run the container
docker run -it --rm -v "$PWD:/workspaces" \
    -v "$CONFIG_DIR:/lpp/data" \
    -v "$DOCKER_HISTFILE:/root/.bash_history" \
    --env-file "$CONFIG_PATH" \
    -w /workspaces "$DOCKER_IMAGE" "$@"

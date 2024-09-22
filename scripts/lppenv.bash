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
        return 1
    fi

    CONFIG_LAST_MODIFIED=$(stat -c %Y "$CONFIG_PATH")
    NOW=$(date +%s)

    if [ $((NOW - CONFIG_LAST_MODIFIED)) -gt 86400 ]; then
        return 1
    fi

    return 0
}

debug_build_image() {
    docker buildx build -t "$DOCKER_IMAGE" "$DOCKER_IMAGE_ROOT"
}

pull_image() {
    docker pull "$DOCKER_IMAGE"
}

check_update() {
    echo "Checking for updates..."
    # If build root is set, build the image
    if [ -z $DOCKER_IMAGE_ROOT ]; then
        pull_image
    else
        debug_build_image
    fi
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
    -w /workspaces "$DOCKER_IMAGE" "$@"

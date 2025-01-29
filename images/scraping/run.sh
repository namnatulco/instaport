# create volume if it doesnt already exist
podman volume create jsoncache --ignore

podman run --volume jsoncache:/cache --rm prod "$1"

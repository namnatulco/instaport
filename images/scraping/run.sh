# create volume if it doesnt already exist
podman volume create jsoncache --ignore

podman run --rm prod --volume jsoncache:/cache "$1"

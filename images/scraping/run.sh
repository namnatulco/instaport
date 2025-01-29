# create volume if it doesnt already exist
podman volume create jsoncache --ignore

podman run --publish 8000:8000/tcp --detach --volume jsoncache:/cache prod

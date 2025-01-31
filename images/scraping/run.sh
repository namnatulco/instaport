# create volume if it doesnt already exist
podman volume create jsoncache --ignore

podman network create backend
#podman run --publish 8000:8000/tcp --detach --volume jsoncache:/cache instaport
podman run --name instaport.prod --network backend --network-alias webapp --detach --volume jsoncache:/cache instaport

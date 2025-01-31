podman build --tag instaport-debug --file ./Dockerfile.debug

podman run --rm -it --volume jsoncache:/cache instaport-debug /bin/sh

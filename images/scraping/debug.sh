podman build --tag instaport-debug --file ./Dockerfile.debug

podman run --rm -it instaport-debug /bin/sh

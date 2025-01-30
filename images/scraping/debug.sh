rm -rf app/
cp -r ../../app .

podman build --tag debug --file ./Dockerfile.debug

podman run --publish 8000:8000/tcp --rm -it --volume jsoncache:/cache debug

cp -ru ../../app .

podman build --tag prod --file ./Dockerfile

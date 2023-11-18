LOCATION = us-west1
PROJECT_ID = zerok-dev
REPOSITORY = stage

VERSION = 0.0.1-alpha
IMAGE = zk-obfuscator
ART_Repo_URI = $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE)
IMG_VER = $(ART_Repo_URI):$(VERSION)
NAME = zk-obfuscator
BUILDER_NAME = multi-platform-builder


build:
	docker build -t ${IMG_VER} .

push:
	docker push ${IMG_VER}

buildAndPush:build push

docker-build-push-multiarch:
	docker buildx rm ${BUILDER_NAME} || true
	docker buildx create --use --platform=linux/arm64,linux/amd64 --name ${BUILDER_NAME}
	docker buildx build --platform=linux/arm64,linux/amd64 --push --tag ${IMG_VER} .
	docker buildx rm ${BUILDER_NAME}

ci-cd-build:
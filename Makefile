LOCATION = us-west1
PROJECT_ID = zerok-dev
REPOSITORY = stage

VERSION = fastApi
IMAGE = zk-obfuscator
ART_Repo_URI = $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE)
IMG_VER = $(ART_Repo_URI):$(VERSION)
NAME = zk-obfuscator


buildAndPush:
	docker build -t ${IMG_VER} .
	docker push ${IMG_VER}

ci-cd-build:
.PHONY: docker-image push

IMAGE := libbypi
REPO := 263893614267.dkr.ecr.eu-west-1.amazonaws.com

TAG := $(shell uname -m)

docker-image:
	docker build -t $(IMAGE) .

push: REMOTE:=$(REPO)/$(IMAGE):$(TAG)
push:
	docker tag $(IMAGE) $(REMOTE)
	docker push $(REMOTE)

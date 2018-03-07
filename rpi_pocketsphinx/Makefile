.PHONY: docker-image push

IMAGE := libbypi
REPO := 263893614267.dkr.ecr.eu-west-1.amazonaws.com

DISTRIBUTOR := $(shell lsb_release -i | expand)
ifeq ($(DISTRIBUTOR),Distributor ID: Raspbian)
BASE := resin/rpi-raspbian
else
BASE := debian
endif

TAG := $(shell uname -m)

docker-image:
	docker build -t $(IMAGE) --build-arg BASE=$(BASE) .

push: REMOTE:=$(REPO)/$(IMAGE):$(TAG)
push:
	docker tag $(IMAGE) $(REMOTE)
	docker push $(REMOTE)

default: docs

.PHONY: docs
docs:
	- docker run --name ms-python-docs-builder -v ${PWD}:/apidocs irakli/redoc-cli:latest && docker rm -f ms-python-docs-builder

.PHONY: start
start:
	- docker run -d --rm --name ms-python-docs -p 3940:80 -v ${PWD}/api.yml:/usr/share/nginx/html/swagger.yaml -e SPEC_URL=swagger.yaml redocly/redoc:v2.0.0-rc.8-1
	- @echo "server started at: http://0.0.0.0:3940"

.PHONY: stop
stop:
	- docker stop ms-python-docs

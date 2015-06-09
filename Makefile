
.PHONY: clean

upload:
	python setup.py sdist upload

install:
	python setup.py install

clean:
	-rm -fR wp_version_checker.egg-info/ build/ dist

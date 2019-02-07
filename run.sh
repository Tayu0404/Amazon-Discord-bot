docker run \
	--name amazon -it --rm --init\
	--env-file=environment_variable.txt\
	-v `pwd`/source:/python \
	amazon_scraiping_bot \
	bin/bash

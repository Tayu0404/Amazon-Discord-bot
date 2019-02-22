docker run \
	--name amazon -it --rm --init\
	--env-file=environment_variable.txt\
	-v `pwd`/source:/python \
	-e "TZ=Asia/Tokyo" \
	-e "PYTHONASYNCIODEBUG=1"\
	amazon_scraiping_bot \
	bin/bash

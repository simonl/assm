while read X
do
	echo `echo $X | ./lambda.py -E -O $1`
done

update-awsglue:
	cp -r modules/aws-glue-libs/awsglue awsglue

init-db:
	poetry run python ./src/initdb.py
# How to install
1. Go to docker directory
1. Go to environment directory. Actually just amb1 is active.
1. docker compose build
1. docker compose up
1. Copy initial sql to postgresql docker `docker cp docker/amb1/0.sql <container_id>:/tmp`
1. Access postgresql docker container
1. psql -U languagebench
1. \i /tmp/0.sql
1. Access python container
1. Go to data directory `cd data`
1. Execute `python import_ticker.py`

# How to execute the docker environment
1. Go to docker directory
1. Go to environment directory. Actually just amb1 is active.
1. docker compose up

# How to execute the language benchmark
1. Execute the docker environment
1. docker ps
1. There is one docker per language plus one for PostgreSQL
1. Access the dockers of the target languages you want to test
1. Go to src directory
1. Execute ./check_cpu_ram.sh <program_to_be_tested>

## Examples of execution
<pre>
# For C program
./check_cpu_ram.sh bulk_insert_5000_per_second

# For Go program
./check_cpu_ram.sh go run bulk_insert_5000_per_second.go

# For Python program
./check_cpu_ram.sh python bulk_insert_5000_per_second.py

# For PHP program
./check_cpu_ram.sh php bulk_insert_5000_per_second.php
</pre>

### How to compile c program (Debian-like instructions)
1. Access C language docker or use your machine if it has GCC
1. It is required to have `apt-get install libpq-dev` installed
1. `gcc bulk_insert_5000_per_second.c -o bulk_insert_5000_per_second -I/usr/include/postgresql -lpq`

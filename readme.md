# How to install
1. Go to docker directory
2. Go to environment directory. Actually just amb1 is active.
3. docker compose build

# How to execute the docker environment
1. Go to docker directory
2. Go to environment directory. Actually just amb1 is active.
3. docker compose up

# How to execute the language benchmark
1. Execute the docker environment
2. docker ps
3. There is one docker per language plus one for PostgreSQL
4. Access the dockers of the target languages you want to test
5. Go to src directory
6. Execute ./check_cpu_ram.sh <program_to_be_tested>

## Examples of execution
<pre>
# For C program
./check_cpu_ram.sh bulk_insert_5000_per_second

# For Go program
./check_cpu_ram.sh bulk_insert_5000_per_second.go

# For Python program
./check_cpu_ram.sh bulk_insert_5000_per_second.py

# For PHP program
./check_cpu_ram.sh bulk_insert_5000_per_second.php
</pre>

### How to compile c program (Debian-like instructions)
1. Access C language docker or use your machine if it has GCC
2. It is required to have `apt-get install libpq-dev` installed
3. gcc bulk_insert_5000_per_second.c -o bulk_insert_5000_per_second -I/usr/include/postgresql -lpq

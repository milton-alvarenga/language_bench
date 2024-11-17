#!/bin/bash

# The first argument is the program to execute, the rest are the arguments
program="$1"
shift  # Removes the first argument (the program name) from the list of arguments

# Initialize new variable
new_program=""

# Map the program to the new variable
case "$program" in
    python)
        new_program="py"
        ;;
    php)
        new_program="php"
        ;;
    go)
        new_program="go"
        ;;
    ./bulk_insert_5000_per_second)
        new_program="c"
        ;;
    *)
        echo "Program not recognized"
        exit 1
        ;;
esac

# Execute the program in the background with the remaining arguments
"$program" "$@" &
PID=$!

# Log file location
LOG_FILE="process_monitor_${new_program}.log"

# Check if the log file exists, if not, create it and add a header
if [ ! -f "$LOG_FILE" ]; then
    echo "current_time|program|cmd|cpu|mem" > "$LOG_FILE"
fi

# Monitor CPU and RAM usage
while ps -p $PID > /dev/null; do
    # Get current time
    current_time=$(date '+%Y-%m-%d %H:%M:%S')

    # Get process stats
    stats=$(ps -p $PID -o %cpu,%mem,cmd --no-headers)

    # Extract CPU, MEM, and CMD
    cpu=$(echo $stats | awk '{print $1}')
    mem=$(echo $stats | awk '{print $2}')
    cmd=$(echo $stats | awk '{for (i=3; i<=NF; i++) printf $i " "; print ""}')

    # Write to log in the desired format
    echo "$current_time|$new_program|$cmd|$cpu|$mem" >> $LOG_FILE

    # Sleep for 1 second
    sleep 1
done

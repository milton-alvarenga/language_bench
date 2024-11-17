#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <libpq-fe.h>
#include <unistd.h>
#include <sys/time.h>

#define BATCH_SIZE 5000
#define LOG_FILE_NAME "bulk_insert_5000_per_second_c.log"

void write_log(FILE *f_log, const char *agent_id, int total_registers_inserted, double time_spent_to_insert) {
    // Get current timestamp
    char timestamp[64];
    struct timeval tv;
    gettimeofday(&tv, NULL);
    struct tm *tm_info = gmtime(&tv.tv_sec);

    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", tm_info);
    sprintf(timestamp + strlen(timestamp), ".%06ld", tv.tv_usec);

    // Environment ID
    const char *environment_id = "amb1";

    // Write log
    fprintf(f_log, "%s|%s|c|%s|%d|%.2f\n", timestamp, agent_id, environment_id, total_registers_inserted, time_spent_to_insert);
    fflush(f_log);
}

void bulk_insert_stock_prices(PGconn *conn) {
    char sql[500000];
    strcpy(sql, "INSERT INTO stock_price (stock_id, price) VALUES ");

    char values[64];
    for (int stock_id = 1; stock_id <= BATCH_SIZE; stock_id++) {
        double price = 100 + stock_id * 0.01;
        sprintf(values, "(%d, %.4f)%s", stock_id, price, stock_id == BATCH_SIZE ? ";" : ", ");
        strcat(sql, values);
    }

    PGresult *res = PQexec(conn, sql);
    if (PQresultStatus(res) != PGRES_COMMAND_OK) {
        fprintf(stderr, "Insert failed: %s\n", PQerrorMessage(conn));
    }
    PQclear(res);
}

int main() {
    // Environment variables for database connection
    const char *DB_HOST = getenv("DB_HOST");
    const char *DB_USER = getenv("DB_USER");
    const char *DB_PASSWORD = getenv("DB_PASSWORD");
    const char *DB_NAME = getenv("DB_NAME");
    const char *DB_PORT = getenv("DB_PORT") ? getenv("DB_PORT") : "5432";

    // Open log file
    FILE *f_log = fopen(LOG_FILE_NAME, "a");
    if (!f_log) {
        perror("Failed to open log file");
        return 1;
    }

    // Write log header if file is empty
    fseek(f_log, 0, SEEK_END);
    if (ftell(f_log) == 0) {
        fprintf(f_log, "current_time|agent_id|language|environment_id|total_registers_inserted|time_spent_to_insert\n");
        fflush(f_log);
    }

    // Connect to PostgreSQL
    char conninfo[256];
    snprintf(conninfo, sizeof(conninfo),
             "host=%s port=%s dbname=%s user=%s password=%s",
             DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD);

    PGconn *conn = PQconnectdb(conninfo);
    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "Connection to database failed: %s\n", PQerrorMessage(conn));
        PQfinish(conn);
        fclose(f_log);
        return 1;
    }

    // Get hostname
    char agent_id[128];
    gethostname(agent_id, sizeof(agent_id));

    // Main loop
    while (1) {
        struct timeval start, end;
        gettimeofday(&start, NULL);

        // Perform bulk insert
        bulk_insert_stock_prices(conn);

        gettimeofday(&end, NULL);
        double elapsed_time = (end.tv_sec - start.tv_sec) * 1000.0 +
                              (end.tv_usec - start.tv_usec) / 1000.0;

        // Write log
        write_log(f_log, agent_id, BATCH_SIZE, elapsed_time);

        printf("Inserted stock prices for %d stocks in %.2f ms\n", BATCH_SIZE, elapsed_time);

        // Sleep to maintain 1-second interval if needed
        if (elapsed_time < 1000) {
            usleep((1000 - elapsed_time) * 1000);
        }
    }

    // Clean up
    PQfinish(conn);
    fclose(f_log);

    return 0;
}

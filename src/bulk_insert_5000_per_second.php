<?php
// Log file name
$logFilePath = "./log/bulk_insert_5000_per_second_php.log";

// Create log file with headers if it doesn't exist
if (!file_exists($logFilePath)) {
    file_put_contents($logFilePath, "current_time|agent_id|language|environment_id|total_registers_inserted|time_spent_to_insert\n");
}

// Open the log file for appending
$f_log = fopen($logFilePath, "a");

// Database credentials from environment variables
$DB_HOST = getenv("DB_HOST");
$DB_USER = getenv("DB_USER");
$DB_PASSWORD = getenv("DB_PASSWORD");
$DB_NAME = getenv("DB_NAME");
$DB_PORT = getenv("DB_PORT") ?: "5432"; // Default PostgreSQL port

// Connect to PostgreSQL
try {
    $dsn = "pgsql:host=$DB_HOST;port=$DB_PORT;dbname=$DB_NAME";
    $conn = new PDO($dsn, $DB_USER, $DB_PASSWORD, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_AUTOCOMMIT => true
    ]);
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}

// Function to write log
function write_log($f_log, $agent_id, $total_registers_inserted, $time_spent_to_insert) {
    $current_time = date("Y-m-d H:i:s.u");
    $environment_id = "amb1";

    $data = [
        $current_time,
        $agent_id,
        'php',
        $environment_id,
        $total_registers_inserted,
        $time_spent_to_insert
    ];

    fwrite($f_log, implode("|", $data) . "\n");
    fflush($f_log);
}

// Function to perform bulk insert
function bulk_insert_stock_prices($conn) {
    // Generate 5000 unique stock_price records
    $records = [];
    for ($stock_id = 1; $stock_id <= 5000; $stock_id++) {
        $price = round(100 + $stock_id * 0.01, 4);
        $records[] = "($stock_id, $price)";
    }

    // Define the SQL for bulk insertion
    $sql = "INSERT INTO stock_price (stock_id, price) VALUES " . implode(", ", $records);

    // Execute the query
    $conn->exec($sql);
}

// Main loop for inserting records
try {
    $batchSize = 5000;
    $agent_id = gethostname();

    while (true) {
        $start_time = microtime(true);

        // Perform the bulk insert
        bulk_insert_stock_prices($conn);

        // Calculate the loop execution time
        $elapsed_time = (microtime(true) - $start_time) * 1000; // Convert to milliseconds

        // Write to log
        write_log($f_log, $agent_id, $batchSize, $elapsed_time);

        echo "Inserted stock prices for $batchSize stocks\n";

        // Sleep to maintain a 1-second interval if needed
        if ($elapsed_time < 1000) {
            usleep((int)(1000 - $elapsed_time) * 1000); // Convert remaining time to microseconds
        }
    }
} catch (Exception $e) {
    echo "Process interrupted or failed: " . $e->getMessage() . "\n";
} finally {
    // Close log file and database connection
    fclose($f_log);
    $conn = null;
    echo "Database connection closed.\n";
}
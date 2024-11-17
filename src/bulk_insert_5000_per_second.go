package main

import (
    "database/sql"
    "fmt"
    "log"
    "math/rand"
    "os"
    "time"
    "strconv"
    "strings"
    //go mod init ambiparbank-bottrader
	//go get github.com/lib/pq
    _ "github.com/lib/pq"
)

func connectToDB() (*sql.DB, error) {
    connStr := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
        os.Getenv("DB_HOST"),
        os.Getenv("DB_USER"),
        os.Getenv("DB_PASSWORD"),
        os.Getenv("DB_NAME"),
        os.Getenv("DB_PORT"),
    )
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        return nil, err
    }

    // Set maximum number of open and idle connections
	db.SetMaxOpenConns(10)  // Adjust this based on your requirements
	db.SetMaxIdleConns(5)   // Adjust this based on your requirements
	db.SetConnMaxLifetime(time.Hour)  // Optional: Recycle connections after a period

    // Check if the connection is available
    if err := db.Ping(); err != nil {
        return nil, err
    }

    fmt.Println("Connected to the database!")
    return db, nil
}


func write_log(f *os.File, totalRegistersInserted int, timeSpentToInsert time.Duration) {
	// Get current time and format it
	currentTime := time.Now()
	formattedTime := currentTime.Format("2006-01-02 15:04:05.000000")

	// Get agent ID (hostname)
	agentID, err := os.Hostname()
	if err != nil {
		log.Fatalf("Error getting hostname: %v", err)
	}

	// Define environment ID
	environmentID := "amb1"

	// Prepare data slice for writing to log
	data := []string{
		formattedTime,
		agentID,
		"go",
		environmentID,
		strconv.Itoa(totalRegistersInserted),
		fmt.Sprintf("%12f", float64(timeSpentToInsert.Seconds()) * 1000),
	}

	// Write data to log file in the specified format
	if _, err := f.WriteString(fmt.Sprintf("%s\n", strings.Join(data, "|"))); err != nil {
		log.Fatalf("Error writing to log file: %v", err)
	}
}


// bulkInsertStockPrices inserts stock prices in bulk into the stock_price table.
func bulkInsertStockPrices(db *sql.DB, startID, endID int) error {
    query := "INSERT INTO stock_price (stock_id, price) VALUES "
    values := []interface{}{}

    for i := startID; i <= endID; i++ {
        price := rand.Float64() * 100 // Random price between 0 and 100
        query += fmt.Sprintf("($%d, $%d),", len(values)+1, len(values)+2)
        values = append(values, i, price)
    }

    // Trim the last comma
    query = query[:len(query)-1]

    // Execute the query
    _, err := db.Exec(query, values...)
    return err
}

func main() {

    logfilenm := "bulk_insert_5000_per_second_go.log"

    // Check if the file exists
    if _, err := os.Stat(logfilenm); os.IsNotExist(err) {
        // Create the file if it doesn't exist
        file, err := os.Create(logfilenm)
        if err != nil {
            fmt.Println("Error creating file:", err)
            return
        }
        defer file.Close()
    
        header := "current_time|agent_id|language|environment_id|total_registers_inserted|time_spent_to_insert\n"
    
        // Write the header to the file
        if _, err := file.WriteString(header); err != nil {
            fmt.Println("Error writing header:", err)
        }
    }


    db, err := connectToDB()
    if err != nil {
        log.Fatalf("Could not connect to database: %v", err)
    }
    defer db.Close()

    startID := 1
    endID := 5000
	// Number of records to insert per loop
    batchSize := 5000

    // Open the file for appending
    f, err := os.OpenFile(logfilenm, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer f.Close()


	for {

		for i := startID; i <= endID; i += batchSize {
			loopStartTime := time.Now()

			batchEndID := i + batchSize - 1
			if batchEndID > endID {
				batchEndID = endID
			}

			if err := bulkInsertStockPrices(db, i, batchEndID); err != nil {
				log.Fatalf("Failed to insert batch: %v", err)
			}           
			elapsed := time.Since(loopStartTime)

			fmt.Printf("Inserted stock prices for stock IDs %d to %d\n", i, batchEndID)


            write_log(f, batchSize, elapsed)

            elapsed_real := time.Since(loopStartTime)

			if elapsed_real < time.Second {
				time.Sleep(time.Second - elapsed_real)
			}
		}
    }
}

CREATE TABLE stock (
    stock_id SERIAL PRIMARY KEY,
    nm TEXT NOT NULL,
    symbol TEXT NOT NULL,
    universal_code TEXT,
    stock_market_id INTEGER REFERENCES stock_market(stock_market_id)
);

CREATE TABLE stock_price (
    stock_price_id BIGSERIAL PRIMARY KEY,
    stock_id INTEGER NOT NULL REFERENCES stock(stock_id),
    price NUMERIC(12, 4) NOT NULL,           -- Adjust precision based on price requirements
    dtc TIMESTAMPTZ NOT NULL DEFAULT NOW()   -- Date and time with time zone for accuracy in time-series data
);
CREATE INDEX idx_stock_price_stockid_datehour ON stock_price(stock_id, dtc);

CREATE TABLE stock_market (
    stock_market_id SERIAL PRIMARY KEY,
    nm TEXT NOT NULL
);

INSERT INTO stock_market (nm) VALUES (
    'b3'
),(
    'nasdaq'
),(
    'nyse'
);
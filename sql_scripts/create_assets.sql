CREATE SCHEMA IF NOT EXISTS staging;

CREATE SCHEMA IF NOT EXISTS prod;

CREATE TABLE IF NOT EXISTS staging.scraped_listings (
    id TEXT PRIMARY KEY,
    scraped_at TIMESTAMP,
    combination_name TEXT NOT NULL,
    link TEXT NOT NULL,
    location TEXT NOT NULL,
    location_detail TEXT,
    size TEXT NOT NULL,
    bedrooms TEXT,
    bathrooms TEXT,
    parking_spaces TEXT,
    price TEXT NOT NULL
);
CREATE SCHEMA IF NOT EXISTS staging;

CREATE SCHEMA IF NOT EXISTS prod;

CREATE TABLE IF NOT EXISTS staging.scraped_listings (
    id SERIAL PRIMARY KEY,
    scraped_at DATE NOT NULL,
    combination_name TEXT NOT NULL,
    listing_id TEXT NOT NULL,
    link TEXT NOT NULL,
    listing_info TEXT NOT NULL,
    region TEXT NOT NULL,
    location_detail TEXT,
    size_m2 INTEGER NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    parking_spaces INTEGER NOT NULL,
    iptu INTEGER,
    condominium_fee INTEGER,
    price INTEGER NOT NULL
);
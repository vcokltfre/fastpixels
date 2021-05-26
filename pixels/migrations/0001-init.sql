CREATE TABLE IF NOT EXISTS Access (
    token               VARCHAR(255) NOT NULL PRIMARY KEY,
    discord_id          BIGINT NOT NULL UNIQUE,
    banned              BOOLEAN NOT NULL DEFAULT FALSE,
    staff               BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS PixelState (
    id                  SERIAL PRIMARY KEY,
    pixels              TEXT NOT NULL
);

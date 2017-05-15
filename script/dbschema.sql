CREATE TABLE article (
  id          INTEGER     PRIMARY KEY   AUTOINCREMENT,
  u_id        VARCHAR(65) NOT NULL,
  title       TEXT        NOT NULL,
  body        TEXT        NOT NULL,
  url         TEXT        NOT NULL,
  created_at  DATETIME    NOT NULL,
  context_b   BOOLEAN     DEFAULT 0,
  parse_b     BOOLEAN     DEFAULT 0,
  CONSTRAINT unique_article UNIQUE (u_id)
);

CREATE TABLE context (
  id          INTEGER,
  context_val DOUBLE,
  FOREIGN KEY(id) REFERENCES article(id)
);

CREATE TABLE parsed_article (
  id          INTEGER     PRIMARY KEY   AUTOINCREMENT,
  a_id        INTEGER,
  parsed      TEXT,
  FOREIGN KEY(a_id) REFERENCES article(id)
);


CREATE TABLE User
(
  user_id       INTEGER  NOT NULL,
  username      TEXT     NULL,
  password      TEXT     NULL,
  email         TEXT     NULL,
  premium_type_id INTEGER NULL,
  PRIMARY KEY (user_id),
  FOREIGN KEY (premium_type_id) REFERENCES PremiumType(premium_type_id)
);

CREATE TABLE PremiumType
(
  premium_type_id INTEGER NOT NULL,
  name            TEXT    NOT NULL,   
  description     TEXT    NULL,      
  price           DOUBLE  NOT NULL,   
  category        TEXT    NOT NULL,  
  PRIMARY KEY (premium_type_id)
);

CREATE TABLE Payment
(
  payment_id      INTEGER  NOT NULL,
  user_id         INTEGER  NOT NULL,
  premium_type_id INTEGER  NOT NULL,    
  payment_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  payment_method  TEXT     NOT NULL, 
  amount_paid     DOUBLE   NOT NULL, 
  status          TEXT     NOT NULL, 
  PRIMARY KEY (payment_id),
  FOREIGN KEY (user_id) REFERENCES User (user_id),
  FOREIGN KEY (premium_type_id) REFERENCES PremiumType (premium_type_id)
);

CREATE TABLE SVG_Source
(
  user_id INTEGER NOT NULL,
  svg_url TEXT    NOT NULL,
  PRIMARY KEY (user_id),
  FOREIGN KEY (user_id) REFERENCES User (user_id)
);
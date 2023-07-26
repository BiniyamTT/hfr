DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS default_images;
DROP TABLE IF EXISTS bookings;

-- SQLite
CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT,
    hash TEXT NOT NULL,
    phoneno TEXT UNIQUE NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usertype INTEGER NOT NULL
);


CREATE TABLE equipment(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    owner_id INTEGER NOT NULL,
    def_img_id INTEGER NOT NULL, 
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    license_plate_no INTEGER NOT NULL,
    fuel_type TEXT NOT NULL,
    hp INTEGER,
    year INTEGER NOT NULL,
    hourly_rate INTEGER NOT NULL,
    advance TEXT INTEGER NULL,
    duration TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user(user_id),
    FOREIGN KEY (def_img_id) REFERENCES default_images(id)
);

CREATE TABLE default_images(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    image_data BLOB NOT NULL
);

CREATE TABLE bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    lessor_id INTEGER NOT NULL,
    lessee_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    booking_status TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    delivery_preference TEXT NOT NULL,
    delivery_address TEXT,
    pickup_location TEXT,
    return_location TEXT,
    lessee_alt_name TEXT,
    lessee_alt_email TEXT,
    lessee_alt_phone TEXT,
    lessee_tin TEXT,
    additional_note TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment (id),
    FOREIGN KEY (lessor_id) REFERENCES equipment (owner_id),
    FOREIGN KEY (lessee_id) REFERENCES user (id)
);




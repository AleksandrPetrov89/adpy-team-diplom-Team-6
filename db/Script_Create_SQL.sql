CREATE TABLE IF NOT EXISTS user_data (
	user_id INTEGER PRIMARY KEY,
	profile_link VARCHAR(60) NOT NULL,
                age INTEGER CHECK(age<150),
	first_name VARCHAR(40),
	last_name VARCHAR(40),
                sex INTEGER,
	city VARCHAR(60),
	token VARCHAR(80),
	groups INTEGER,
                interests VARCHAR(100),
	music VARCHAR(100),
	books VARCHAR(100),
                photo_link_1 VARCHAR(60) NOT NULL,
	photo_link_2 VARCHAR(60) NOT NULL,
                photo_link_3 VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS elected_list (
                user_data_user_id INTEGER NOT NULL REFERENCES user_data(user_id),
	bot_user_user_id INTEGER NOT NULL REFERENCES user_data(user_id)
);

CREATE TABLE IF NOT EXISTS black_list (
	user_data_user_id INTEGER NOT NULL REFERENCES user_data(user_id)
	bot_user_user_id INTEGER NOT NULL REFERENCES user_data(user_id)
);
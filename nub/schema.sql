DROP TABLE IF EXISTS VIDEO_DATA;
CREATE TABLE VIDEO_DATA(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	video_id TEXT NOT NULL,
	title TEXT,
	upload_date TEXT,
	duration TEXT,
	description TEXT,
	genre TEXT,
	is_paid INTEGER,
	is_unlisted INTEGER,
	is_family_friendly INTEGER,
	channel_id TEXT,
	views INTEGER,
	likes INTEGER,
	dislikes INTEGER,
	regionsAllowed INTEGER,
	thumbnail_url TEXT,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS TRANSCRIPT;
CREATE TABLE TRANSCRIPT(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	video_id TEXT NOT NULL,
	url TEXT NOT NULL,
	language_code TEXT NOT NULL DEFAULT 'en',
	is_generated INTEGER NOT NULL DEFAULT 1,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS TRANSCRIPT_TEXT;
CREATE TABLE TRANSCRIPT_TEXT(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	video_id TEXT NOT NULL,
	text_data TEXT,
	start_time REAL,
	duration REAL
);

DROP TABLE IF EXISTS TRANSCRIPT_FULL_TEXT;
CREATE TABLE TRANSCRIPT_FULL_TEXT(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	video_id TEXT NOT NULL,
	language TEXT NOT NULL,
	data TEXT,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS CHAT_RESPONSE;
CREATE TABLE CHAT_RESPONSE(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	model TEXT NOT NULL,
	message_role TEXT,
	message_content TEXT,
	done_reason TEXT,
	done INTEGER,
	total_duration INTEGER,
	load_duration INTEGER,
	prompt_eval_count INTEGER,
	prompt_eval_duration INTEGER,
	eval_count INTEGER,
	eval_duration INTEGER,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

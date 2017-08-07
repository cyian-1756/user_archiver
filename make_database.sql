CREATE TABLE `userinfo` (
        `uid` INTEGER PRIMARY KEY AUTOINCREMENT,
        `author` VARCHAR(64) NULL,
        `subreddit` VARCHAR(64) NULL,
        `subreddit_id` VARCHAR(64) NULL,
        `comment_id` VARCHAR(64),
        `link_title` VARCHAR(64),
        `author_flair_text` VARCHAR(64),
        `body` TEXT,
        `created` INT,
        `score` INT
    );

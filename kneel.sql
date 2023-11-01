-- Run this block if you already have a database and need to re-create it
DELETE FROM Metals;
DELETE FROM Styles;
DELETE FROM Sizes;
DELETE FROM Orders;

DROP TABLE IF EXISTS Metals;
DROP TABLE IF EXISTS Styles;
DROP TABLE IF EXISTS Sizes;
DROP TABLE IF EXISTS Orders;
-- End block

CREATE TABLE IF NOT EXISTS `Metal`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS `Style`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS `Size`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NUMERIC(5,2) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS `Order`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal_id` INTEGER NOT NULL,
    `style_id` INTEGER NOT NULL,
    `size_id` INTEGER NOT NULL,
    `time_stamp` DATE NOT NULL,
    FOREIGN KEY(`metal_id`) REFERENCES `Metal`(`id`),
    FOREIGN KEY(`style_id`) REFERENCES `Style`(`id`),
    FOREIGN KEY(`size_id`) REFERENCES `Size`(`id`)
);

INSERT INTO `Metal` (`metal`, `price`) VALUES ('Gold', 1000);
INSERT INTO `Metal` (`metal`, `price`) VALUES ('Silver', 500);
INSERT INTO `Metal` (`metal`, `price`) VALUES ('Bronze', 250);

INSERT INTO `Style` (`style`, `price`) VALUES ('Princess', 1000);
INSERT INTO `Style` (`style`, `price`) VALUES ('Teardrop', 500);
INSERT INTO `Style` (`style`, `price`) VALUES ('Oval', 250);

INSERT INTO `Size` (`carets`, `price`) VALUES ('14k', 1000);
INSERT INTO `Size` (`carets`, `price`) VALUES ('10k', 500);
INSERT INTO `Size` (`carets`, `price`) VALUES ('7k', 250);

INSERT INTO `Order` (`metal_id`, `style_id`, `size_id`, `time_stamp`) VALUES
(2, 2, 2, '2023-10-30');

INSERT INTO `Order` (`metal_id`, `style_id`, `size_id`, `time_stamp`) VALUES
(1, 3, 2, '2023-10-30');
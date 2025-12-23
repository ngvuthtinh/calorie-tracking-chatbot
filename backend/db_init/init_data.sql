-- =========================================
-- SETUP CHARSET & DB
-- =========================================
SET NAMES utf8mb4;
SET time_zone = '+07:00'; 
USE calorie_db;

-- Tạo user (nếu chưa có) và cho phép kết nối từ mọi IP (%)
-- Lưu ý: Nếu user được tạo tự động bởi biến môi trường docker-compose, 
-- dòng này sẽ đảm bảo cấp lại quyền cho chắc chắn.
CREATE USER IF NOT EXISTS 'calorie_user'@'%' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON calorie_db.* TO 'calorie_user'@'%';
FLUSH PRIVILEGES;

-- =========================================
-- 0) USERS
-- =========================================
CREATE TABLE users (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
email VARCHAR(255) UNIQUE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- 1) PROFILE (1 row per user)
-- =========================================
CREATE TABLE user_profile (
user_id BIGINT PRIMARY KEY,
height_cm INT NULL,
weight_kg DECIMAL(5,2) NULL,
age INT NULL,
gender VARCHAR(10) NULL,
activity_level ENUM('low','moderate','high') NULL,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
CONSTRAINT fk_profile_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- =========================================
-- 2) GOAL (1 active goal per user for MVP)
-- - goal_type: lose / maintain / gain
-- - target_weight_kg: optional
-- - daily_target_kcal: cached for fast "today remaining"
-- =========================================
CREATE TABLE user_goal (
user_id BIGINT PRIMARY KEY,
goal_type ENUM('lose','maintain','gain') NOT NULL,
target_weight_kg DECIMAL(5,2) NULL,
target_delta_kg DECIMAL(5,2) NULL,
daily_target_kcal INT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
CONSTRAINT fk_goal_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- =========================================
-- 3) DAY SESSION (1 user x 1 date)
-- =========================================
CREATE TABLE day_session (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
user_id BIGINT NOT NULL,
entry_date DATE NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
UNIQUE KEY uq_user_date (user_id, entry_date),
INDEX idx_user_date (user_id, entry_date),
CONSTRAINT fk_day_user FOREIGN KEY (user_id) REFERENCES users(id)
);

-- =========================================
-- 4) FOOD LOGGING
-- One food_entry per command, contains meal/action
-- food_item contains qty/unit/name as user typed
-- Later you can map item to catalog to compute kcal
-- =========================================
CREATE TABLE food_entry (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
day_session_id BIGINT NOT NULL,
entry_code VARCHAR(20) NOT NULL,   -- "f1", "f2" (scoped per day)
meal ENUM('breakfast','lunch','dinner','snack') NULL,
action ENUM('eat','drink') NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
is_deleted BOOLEAN DEFAULT FALSE,
UNIQUE KEY uq_food_code_per_day (day_session_id, entry_code),
INDEX idx_food_day (day_session_id, created_at),
CONSTRAINT fk_food_day FOREIGN KEY (day_session_id) REFERENCES day_session(id)
);

CREATE TABLE food_item (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
food_entry_id BIGINT NOT NULL,
item_name VARCHAR(255) NOT NULL,      -- raw normalized name (e.g. "egg")
qty DECIMAL(10,2) NULL,
unit VARCHAR(50) NULL,                -- "g", "cup", "piece", ...
note VARCHAR(255) NULL,
-- optional mapping to catalog (for later)
catalog_food_id BIGINT NULL,
CONSTRAINT fk_food_item_entry FOREIGN KEY (food_entry_id) REFERENCES food_entry(id),
INDEX idx_food_item_entry (food_entry_id),
INDEX idx_food_item_name (item_name)
);

-- =========================================
-- 5) EXERCISE LOGGING
-- exercise_entry per command
-- exercise_item includes duration/distance/reps fields
-- =========================================
CREATE TABLE exercise_entry (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
day_session_id BIGINT NOT NULL,
entry_code VARCHAR(20) NOT NULL,     -- "x1", "x2"
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
is_deleted BOOLEAN DEFAULT FALSE,
UNIQUE KEY uq_ex_code_per_day (day_session_id, entry_code),
INDEX idx_ex_day (day_session_id, created_at),
CONSTRAINT fk_ex_day FOREIGN KEY (day_session_id) REFERENCES day_session(id)
);

CREATE TABLE exercise_item (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
exercise_entry_id BIGINT NOT NULL,
ex_type VARCHAR(50) NOT NULL,        -- "run", "walk", "pushups", ...
duration_min INT NULL,
distance_km DECIMAL(6,2) NULL,
reps INT NULL,
note VARCHAR(255) NULL,
catalog_exercise_id BIGINT NULL,
CONSTRAINT fk_ex_item_entry FOREIGN KEY (exercise_entry_id) REFERENCES exercise_entry(id),
INDEX idx_ex_item_entry (exercise_entry_id),
INDEX idx_ex_item_type (ex_type)
);

-- =========================================
-- 6) FOOD CATALOG (nutrition database)
-- Keep it simple: kcal per base_unit
-- base_unit examples: "g", "ml", "piece", "cup"
-- grams_per_unit lets you convert "cup" -> grams if needed
-- =========================================
CREATE TABLE food_catalog (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
name_normalized VARCHAR(255) NOT NULL UNIQUE,  -- "egg", "milk", "pho_bo"
kcal_per_unit DECIMAL(10,2) NOT NULL,
base_unit VARCHAR(50) NOT NULL,
grams_per_unit DECIMAL(10,2) NULL,
source VARCHAR(100) NULL
);

CREATE TABLE food_alias (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
alias_normalized VARCHAR(255) NOT NULL UNIQUE, -- "pho bò", "phobo"
food_id BIGINT NOT NULL,
CONSTRAINT fk_alias_food FOREIGN KEY (food_id) REFERENCES food_catalog(id)
);

-- =========================================
-- 7) EXERCISE CATALOG (MET or kcal rule)
-- MVP: store MET; burned_kcal = MET * weight_kg * duration_hr
-- For reps-based, you can store kcal_per_rep (optional)
-- =========================================
CREATE TABLE exercise_catalog (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
name_normalized VARCHAR(50) NOT NULL UNIQUE,   -- "run", "walk", "pushups"
met_light DECIMAL(5,2) NULL,
met_moderate DECIMAL(5,2) NULL,
met_heavy DECIMAL(5,2) NULL,
kcal_per_rep DECIMAL(10,4) NULL
);

-- =========================================
-- 8) ACTION LOG (optional but great for undo)
-- Stores what action happened, on which entry, at what time
-- Undo can simply revert last action for a day_session
-- =========================================
CREATE TABLE action_log (
id BIGINT AUTO_INCREMENT PRIMARY KEY,
day_session_id BIGINT NOT NULL,
action_type ENUM('create_food','edit_food','delete_food',
'create_exercise','edit_exercise','delete_exercise',
'update_profile','update_goal') NOT NULL,
ref_table VARCHAR(50) NOT NULL,   -- "food_entry", "exercise_entry"
ref_id BIGINT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
INDEX idx_action_day_time (day_session_id, created_at),
CONSTRAINT fk_action_day FOREIGN KEY (day_session_id) REFERENCES day_session(id)
);


INSERT INTO food_catalog (name_normalized, kcal_per_unit, base_unit, grams_per_unit, source)
VALUES
-- Basic foods
('egg', 72, 'piece', NULL, 'MVP'),
('milk', 42, '100ml', 100, 'MVP'),
('yogurt', 60, '100g', 100, 'MVP'),
('banana', 105, 'piece', NULL, 'MVP'),
('apple', 95, 'piece', NULL, 'MVP'),
('orange', 62, 'piece', NULL, 'MVP'),
('bread', 80, 'slice', NULL, 'MVP'),
('rice_cooked', 130, '100g', 100, 'MVP'),
('noodle_cooked', 138, '100g', 100, 'MVP'),
-- Meat / protein
('chicken_breast', 165, '100g', 100, 'MVP'),
('pork_lean', 242, '100g', 100, 'MVP'),
('beef_lean', 250, '100g', 100, 'MVP'),
('fish', 206, '100g', 100, 'MVP'),
('tofu', 76, '100g', 100, 'MVP'),
-- Fast food / common meals
('pizza', 285, '100g', 100, 'MVP'),
('hamburger', 295, '100g', 100, 'MVP'),
('fried_rice', 190, '100g', 100, 'MVP'),
('salad', 33, '100g', 100, 'MVP'),
-- Drinks
('coffee_black', 2, 'cup', NULL, 'MVP'),
('tea_unsweetened', 0, 'cup', NULL, 'MVP'),
('coconut_water', 19, '100ml', 100, 'MVP'),
-- Vietnamese foods (approx for demo)
('pho_bo', 450, 'bowl', NULL, 'MVP'),
('banh_mi', 450, 'piece', NULL, 'MVP'),
('com_tam', 700, 'plate', NULL, 'MVP'),
('bun_bo_hue', 550, 'bowl', NULL, 'MVP'),
('hu_tieu', 480, 'bowl', NULL, 'MVP'),
('spring_rolls', 140, 'piece', NULL, 'MVP');

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'eggs', id FROM food_catalog WHERE name_normalized = 'egg';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'milk (fresh)', id FROM food_catalog WHERE name_normalized = 'milk';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'pho bò', id FROM food_catalog WHERE name_normalized = 'pho_bo';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'phobo', id FROM food_catalog WHERE name_normalized = 'pho_bo';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'bánh mì', id FROM food_catalog WHERE name_normalized = 'banh_mi';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'cơm tấm', id FROM food_catalog WHERE name_normalized = 'com_tam';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'bún bò huế', id FROM food_catalog WHERE name_normalized = 'bun_bo_hue';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'hủ tiếu', id FROM food_catalog WHERE name_normalized = 'hu_tieu';

INSERT INTO food_alias (alias_normalized, food_id)
SELECT 'coconut water', id FROM food_catalog WHERE name_normalized = 'coconut_water';


INSERT INTO exercise_catalog (name_normalized, met_light, met_moderate, met_heavy, kcal_per_rep)
VALUES
-- Duration-based (MET)
('run', 6.0, 9.0, 12.5, NULL),
('walk', 2.5, 3.5, 5.0, NULL),
('cycling', 5.5, 7.5, 10.0, NULL),
('swim', 6.0, 8.0, 11.0, NULL),
('plank', 3.0, 4.0, 5.0, NULL),
-- Reps-based (rough MVP values)
('pushups', NULL, NULL, NULL, 0.5),
('squats',  NULL, NULL, NULL, 0.6),
('lunges',  NULL, NULL, NULL, 0.6);


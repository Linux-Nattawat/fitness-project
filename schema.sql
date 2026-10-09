-- ============================================================
-- schema.sql -- ระบบฟิตเนส / คลาสออกกำลังกาย (Fitness Class)
-- กติกา: การจอง = M:N (member x gym_class), อุปกรณ์ต่อคลาส = M:N (gym_class x equipment),
--        แต่ละคลาสมีเทรนเนอร์ (1:M จาก trainer)
-- ============================================================

-- ลบตารางเดิมออกก่อนตามลำดับ (ป้องกันปัญหาติด Foreign Key เวลาสร้างใหม่)
DROP TABLE IF EXISTS class_equipment;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS gym_class;
DROP TABLE IF EXISTS trainer;
DROP TABLE IF EXISTS member;

CREATE TABLE member (
    member_id   INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    gender      VARCHAR(10),
    join_date   DATE NOT NULL,
    package_type ENUM('รายวัน', 'รายเดือน', 'รายปี') NOT NULL DEFAULT 'รายเดือน'
);

CREATE TABLE trainer (
    trainer_id  INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    specialty   VARCHAR(100),
    phone       VARCHAR(20),
    supervisor_id INT NULL,
    FOREIGN KEY (supervisor_id) REFERENCES trainer(trainer_id) ON DELETE SET NULL
);

CREATE TABLE gym_class (
    class_id    INT AUTO_INCREMENT PRIMARY KEY,
    trainer_id  INT NOT NULL,
    name        VARCHAR(100) NOT NULL,
    room        VARCHAR(50),
    capacity    INT NOT NULL,
    schedule_time DATETIME NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id) ON DELETE RESTRICT
);

CREATE TABLE booking (
    booking_id  INT AUTO_INCREMENT PRIMARY KEY,
    member_id   INT NOT NULL,
    class_id    INT NOT NULL,
    book_date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('confirmed', 'attended', 'cancelled') DEFAULT 'confirmed',
    FOREIGN KEY (member_id) REFERENCES member(member_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES gym_class(class_id) ON DELETE CASCADE
);

CREATE TABLE equipment (
    equip_id    INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    zone        VARCHAR(50),
    status      VARCHAR(50) DEFAULT 'พร้อมใช้งาน',
    total_quantity INT NOT NULL DEFAULT 0 
);

CREATE TABLE class_equipment (
    class_id    INT NOT NULL,
    equip_id    INT NOT NULL,
    quantity    INT NOT NULL,
    PRIMARY KEY (class_id, equip_id),
    FOREIGN KEY (class_id) REFERENCES gym_class(class_id) ON DELETE CASCADE,
    FOREIGN KEY (equip_id) REFERENCES equipment(equip_id) ON DELETE CASCADE
);

INSERT INTO trainer (trainer_id, name, specialty, phone, supervisor_id) VALUES
(1, 'สมชาย สายลุย', 'มวยไทย / คาร์ดิโอ', '081-111-1111', NULL),
(2, 'วิภาวดี สุขภาพดี', 'โยคะ / พิลาทิส', '082-222-2222', 1),
(3, 'อานนท์ กล้ามโต', 'เวทเทรนนิ่ง / เพาะกาย', '083-333-3333', 1),
(4, 'เจนจิรา ฟิตเปรี๊ยะ', 'ซุมบ้า / แดนซ์', '084-444-4444', 2),
(5, 'ณัฐพล ขี่พายุ', 'สปินนิ่งไบค์ / HIIT', '085-555-5555', 1),
(6, 'ชัชวาลย์ ยืดเหยียด', 'ยืดกล้ามเนื้อ / กายภาพ', '086-666-6666', 2);

INSERT INTO member (member_id, name, gender, join_date, package_type) VALUES
(1, 'ธนกฤต ชัยชนะ', 'ชาย', '2026-01-10', 'รายปี'),
(2, 'ศิริพร บุญมี', 'หญิง', '2026-02-15', 'รายเดือน'),
(3, 'กิตติศักดิ์ เจริญ', 'ชาย', '2026-03-01', 'รายปี'),
(4, 'พิมพาพร ยิ้มสวย', 'หญิง', '2026-04-12', 'รายเดือน'),
(5, 'วรเมธ คงกระพัน', 'ชาย', '2026-05-20', 'รายวัน'),
(6, 'ชลธิชา สว่างวงศ์', 'หญิง', '2026-06-11', 'รายเดือน'),
(7, 'ปวริศ มั่งคั่ง', 'ชาย', '2026-07-05', 'รายวัน'),
(8, 'นภัสสร อ่อนหวาน', 'หญิง', '2026-08-18', 'รายปี');

INSERT INTO gym_class (class_id, trainer_id, name, room, capacity, schedule_time) VALUES
(1, 1, 'มวยไทยเบิร์นไขมัน', 'Studio A', 20, '2026-10-01 09:00:00'),
(2, 2, 'โยคะยามเช้า', 'Studio B', 15, '2026-10-01 10:30:00'),
(3, 3, 'บอดี้พัมป์สร้างกล้าม', 'Weight Room', 12, '2026-10-01 13:00:00'),
(4, 4, 'ซุมบ้าแดนซ์สุดมันส์', 'Studio A', 25, '2026-10-01 17:00:00'),
(5, 5, 'สปินนิ่งไบค์ปั่นแหลก', 'Cycling Room', 15, '2026-10-01 18:30:00'),
(6, 1, 'มวยไทยแอดวานซ์', 'Studio A', 15, '2026-10-02 18:00:00');

INSERT INTO equipment (equip_id, name, zone, status, total_quantity) VALUES
(1, 'นวมชกมวย', 'Boxing Zone', 'พร้อมใช้งาน', 30),
(2, 'เชือกกระโดด', 'Boxing Zone', 'พร้อมใช้งาน', 25),
(3, 'เสื่อโยคะ', 'Yoga Zone', 'พร้อมใช้งาน', 20),
(4, 'บล็อกโยคะ', 'Yoga Zone', 'พร้อมใช้งาน', 15),
(5, 'ดัมเบล 5kg', 'Weight Zone', 'พร้อมใช้งาน', 20),
(6, 'สเต็ปแอโรบิก', 'Studio A', 'พร้อมใช้งาน', 25);

INSERT INTO class_equipment (class_id, equip_id, quantity) VALUES
(1, 1, 20), 
(1, 2, 20), 
(2, 3, 15), 
(2, 4, 15), 
(3, 5, 12), 
(4, 6, 25), 
(6, 1, 15), 
(6, 2, 15);

INSERT INTO booking (member_id, class_id, book_date, status) VALUES
(1, 1, '2026-09-28 08:30:00', 'confirmed'),
(2, 1, '2026-09-28 09:00:00', 'confirmed'),
(3, 1, '2026-09-28 09:15:00', 'attended'),
(4, 1, '2026-09-28 09:20:00', 'confirmed'),
(1, 2, '2026-09-28 09:30:00', 'confirmed'),
(4, 2, '2026-09-28 09:45:00', 'attended'),
(5, 3, '2026-09-28 10:00:00', 'confirmed'),
(6, 3, '2026-09-28 10:15:00', 'confirmed'),
(2, 4, '2026-09-28 10:30:00', 'confirmed'),
(3, 4, '2026-09-28 11:00:00', 'confirmed'),
(7, 4, '2026-09-28 11:15:00', 'cancelled'),
(8, 4, '2026-09-28 11:30:00', 'confirmed'),
(1, 5, '2026-09-28 12:00:00', 'confirmed'),
(2, 6, '2026-09-28 12:30:00', 'confirmed'),
(3, 6, '2026-09-28 13:00:00', 'confirmed');



-- Hello World, My name is Linux
-- im the owner of this Project with my friend Sumolnwza007
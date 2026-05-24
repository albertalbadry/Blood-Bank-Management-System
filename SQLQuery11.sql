CREATE DATABASE bloodbank;



CREATE TABLE Delivery(
    delivery_id INT PRIMARY KEY,
    departure_time DATE,
    arrival_time DATE,
    status VARCHAR(20),
    CHECK (status IN ('Scheduled','In Transit','Completed','Cancelled'))
);

CREATE TABLE Bloodunit(
    unit_id INT PRIMARY KEY,
    collectiondate DATE NOT NULL,
    expirydate DATE NOT NULL,
    status VARCHAR(20),
    delivery_id INT,
    FOREIGN KEY (delivery_id) 
    REFERENCES Delivery(delivery_id),
    CHECK (status IN ('available','used','expired'))
);

CREATE TABLE bloodtype(
    Bloodtype_id INT PRIMARY KEY,
    Bloodgroup VARCHAR(2) NOT NULL,
    RHfactor CHAR(1) NOT NULL,

    unit_id INT,
    FOREIGN KEY (unit_id) 
    REFERENCES Bloodunit(unit_id),

    CHECK (Bloodgroup IN ('A','B','AB','O')),
    CHECK (RHfactor IN ('+','-'))
);


CREATE TABLE Van(
    van_id INT PRIMARY KEY,
    plate_number VARCHAR(10) NOT NULL,
    capacity INT,
    status VARCHAR(20),
    current_location VARCHAR(20),

    delivery_id INT,
    Foreign KEY (delivery_id)
    REFERENCES Delivery(delivery_id),


);

CREATE TABLE Bloodrequest(
    request_id INT PRIMARY KEY,
    request_date DATE,
    quantity INT NOT NULL,
    Priority VARCHAR(20),
    status VARCHAR(20),

    bloodtype_id INT,
    delivery_id INT,
    Foreign KEY (bloodtype_id)
    REFERENCES bloodtype(Bloodtype_id),
    FOREIGN KEY (delivery_id)
    REFERENCES Delivery(delivery_id),

    CHECK (Priority IN ('Normal','Urgent','Emergency')),

    CHECK (status IN ('Pending','Approved','Rejected'))
);

CREATE TABLE hospital(
    hospital_id INT PRIMARY KEY,
    hospital_name VARCHAR(20),
    location VARCHAR(20),
    phone VARCHAR(15),
    request_id INT,

    FOREIGN KEY (request_id)
    REFERENCES Bloodrequest(request_id)
);


USE bloodbank;


INSERT INTO Delivery VALUES
(1, '2026-05-01', '2026-05-01', 'Completed'),
(2, '2026-05-02', '2026-05-02', 'In Transit'),
(3, '2026-05-03', '2026-05-03', 'Scheduled'),
(4, '2026-05-04', '2026-05-04', 'Completed'),
(5, '2026-05-05', '2026-05-05', 'Cancelled');


INSERT INTO Bloodunit VALUES
(101, '2026-04-01', '2026-07-01', 'available', 1),
(102, '2026-04-05', '2026-07-05', 'used', 1),
(103, '2026-04-07', '2026-07-07', 'available', 2),
(104, '2026-04-10', '2026-07-10', 'expired', 2),
(105, '2026-04-12', '2026-07-12', 'available', 3),
(106, '2026-04-15', '2026-07-15', 'used', 4),
(107, '2026-04-18', '2026-07-18', 'available', 4),
(108, '2026-04-20', '2026-07-20', 'available', 5);


INSERT INTO bloodtype VALUES
(1, 'A', '+', 101),
(2, 'A', '-', 102),
(3, 'B', '+', 103),
(4, 'B', '-', 104),
(5, 'AB', '+', 105),
(6, 'O', '+', 106),
(7, 'O', '-', 107),
(8, 'AB', '-', 108);


INSERT INTO Van VALUES
(1, 'ABC123', 50, 'Active', 'Cairo', 1),
(2, 'DEF456', 40, 'Active', 'Giza', 2),
(3, 'GHI789', 60, 'Maintenance', 'Alexandria', 3),
(4, 'JKL321', 45, 'Active', 'Tanta', 4),
(5, 'MNO654', 55, 'Inactive', 'Mansoura', 5);

INSERT INTO Bloodrequest VALUES
(1, '2026-05-01', 5, 'Urgent', 'Approved', 1, 1),
(2, '2026-05-02', 3, 'Normal', 'Pending', 2, 2),
(3, '2026-05-03', 10, 'Emergency', 'Approved', 3, 3),
(4, '2026-05-04', 2, 'Normal', 'Rejected', 4, 4),
(5, '2026-05-05', 7, 'Urgent', 'Approved', 5, 5),
(6, '2026-05-06', 4, 'Emergency', 'Pending', 6, 1),
(7, '2026-05-07', 6, 'Normal', 'Approved', 7, 2),
(8, '2026-05-08', 8, 'Urgent', 'Pending', 8, 3);





INSERT INTO hospital VALUES
(1, 'El Salam', 'Cairo', '01011111111', 1),
(2, 'Al Noor', 'Giza', '01022222222', 2),
(3, '57357', 'Cairo', '01033333333', 3),
(4, 'Al Amal', 'Alex', '01044444444', 4),
(5, 'Dar El Fouad', 'Giza', '01055555555', 5),
(6, 'El Hayat', 'Tanta', '01066666666', 6),
(7, 'Misr Intl', 'Mansoura', '01077777777', 7),
(8, 'Al Shifa', 'Cairo', '01088888888', 8);


INSERT INTO Delivery VALUES
(10, '2026-06-01', '2026-06-01', 'Completed'),
(11, '2026-06-02', NULL, 'In Transit'),
(12, NULL, NULL, 'Scheduled');

INSERT INTO Bloodunit VALUES
(201, '2026-05-01', '2026-08-01', 'available', 10),
(202, '2026-05-03', '2026-08-03', 'used', NULL),
(203, '2026-05-05', '2026-08-05', 'expired', 11),
(204, '2026-05-07', '2026-08-07', 'available', NULL);

INSERT INTO bloodtype VALUES
(20, 'A', '+', 201),
(21, 'B', '-', NULL),
(22, 'O', '+', 202),
(23, 'AB', '-', NULL);

INSERT INTO Van VALUES
(30, 'CAR111', 40, 'Active', 'Cairo', 10),
(31, 'CAR222', 50, 'Inactive', NULL, NULL),
(32, 'CAR333', 35, 'Maintenance', 'Giza', 11);

INSERT INTO Bloodrequest VALUES
(40, '2026-06-01', 5, 'Urgent', 'Approved', 20, 10),
(41, '2026-06-02', 2, 'Normal', 'Pending', 21, NULL),
(42, NULL, 8, 'Emergency', 'Rejected', 22, 11),
(43, '2026-06-04', 4, 'Normal', 'Pending', 23, NULL);

INSERT INTO hospital VALUES
(50, 'El Salam', 'Cairo', '01011111111', 40),
(51, '57357', 'Cairo', NULL, NULL),
(52, 'Al Noor', NULL, '01033333333', 41),
(53, 'Dar El Fouad', 'Giza', NULL, 42);

------------------------------------------------
USE bloodbank;
SELECT request_id ,hospital_id, hospital_name,location, phone

from hospital
where request_id is null;

SELECT *
FROM Bloodrequest
ORDER BY quantity DESC;


SELECT hospital_id, hospital_name,quantity
FROM hospital h
right outer join Bloodrequest b
on h.request_id =b.request_id
order by quantity desc;

SELECT COUNT(*) AS total_blood_unit
FROM Bloodunit
WHERE status ='used';

SELECT priority , COUNT(*) AS total_requests
From Bloodrequest
group by priority;

SELECT d.status ,count(*) AS total_deliveries 
from Delivery d
inner join Bloodrequest b
on d.delivery_id = b.delivery_id

group by d.status;

SELECT hospital_name,quantity,priority
from hospital h
 inner join Bloodrequest b
on h.request_id = b.request_id;


SELECT br.request_id,
       bt.Bloodgroup,
       bt.RHfactor
FROM Bloodrequest br
INNER JOIN bloodtype bt
ON br.bloodtype_id = bt.Bloodtype_id;

SELECT hospital_name, location ,Bloodgroup, RHfactor
from hospital h
inner join Bloodrequest br
on h.request_id = br.request_id
inner join bloodtype bt
on br.bloodtype_id = bt.Bloodtype_id
where h.location = 'Cairo';


SELECT *
from Bloodunit b
left outer join Delivery d
on b.delivery_id=d.delivery_id;

SELECT *
FROM van v
RIGHT OUTER JOIN Delivery d
on v.delivery_id = d.delivery_id;

SELECT h.hospital_name,
       br.request_id
FROM hospital h
FULL JOIN Bloodrequest br
ON h.request_id = br.request_id;

SELECT *
FROM hospital
WHERE hospital_name LIKE '%El%';

SELECT request_id,
       quantity,
       CASE
           WHEN quantity >= 8 THEN 'High'
           WHEN quantity >= 4 THEN 'Medium'
           ELSE 'Low'
       END AS RequestLevel
FROM Bloodrequest;

SELECT hospital_name,
COALESCE(phone,'NO PHONE') AS ContactNumber
FROM hospital;

SELECT *
FROM Bloodrequest
WHERE quantity> (SELECT AVG(quantity) FROM Bloodrequest);

--------------------------------------

INSERT INTO hospital VALUES
(60, 'Al hayah', 'Cairo', '01099999999', 40);


INSERT INTO Bloodrequest (request_id, request_date, quantity, Priority, status, bloodtype_id, delivery_id)
VALUES (50, GETDATE(), 12, 'Emergency', 'Approved', 20, 10);


UPDATE Bloodunit
SET status = 'used'
WHERE unit_id = 201;

TRUNCATE TABLE EmergencyRequests;

use bloodbank;
------------
SELECT *
FROM Bloodrequest
where quantity = (SELECT MAX(quantity) FROM Bloodrequest);

SELECT request_id, quantity
FROM Bloodrequest
WHERE quantity< All (SELECT quantity from Bloodrequest where Priority='Emergency');

SELECT bloodtype_id,count(*) AS total_requests
from Bloodrequest
group by bloodtype_id
having count(*)>1;


ALTER TABLE hospital
ALTER COLUMN hospital_name VARCHAR(50) NOT NULL;
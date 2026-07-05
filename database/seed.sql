INSERT INTO patients (full_name, email, phone, date_of_birth)
VALUES
('Test Patient One', 'patient1@example.com', '0400000001', '1995-04-12'),
('Test Patient Two', 'patient2@example.com', '0400000002', '1998-09-21');

INSERT INTO doctors (full_name, specialization, email)
VALUES
('Dr Sarah Mitchell', 'General Practitioner', 'sarah.mitchell@example.com'),
('Dr James Wilson', 'Cardiology', 'james.wilson@example.com');

INSERT INTO appointments (patient_id, doctor_id, appointment_date, status)
VALUES
(1, 1, '2026-07-06 10:00:00', 'scheduled'),
(2, 2, '2026-07-06 14:30:00', 'scheduled');
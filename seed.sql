INSERT INTO APP_USER (user_id, given_name, surname, email, affiliation, country, phone_number) 
VALUES
('00000000-0000-0000-0000-000000000001', 'Arman', 'Armanov', 'arman.armanov@example.com', 'Nazarbayev University', 'Kazakhstan', '+77010000001'),
('00000000-0000-0000-0000-000000000002', 'Amina', 'Aminova', 'amina.aminova@example.com', 'Satpayev University', 'Kazakhstan', '+77010000002'),
('00000000-0000-0000-0000-000000000003', 'Dana',    'Serikova',  'dana.serikova@example.com',   'Kazakh-British Technical University', 'Kazakhstan',     '+77011110003'),
('00000000-0000-0000-0000-000000000004', 'Timur',   'Bekov',     'timur.bekov@example.com',     'Al-Farabi Kazakh National University','Kazakhstan',     '+77011110004'),
('00000000-0000-0000-0000-000000000005', 'Aigerim', 'Nurlanova', 'aigerim.nurlanova@example.com','Nazarbayev University',              'Kazakhstan',     '+77011110005'),
('00000000-0000-0000-0000-000000000006', 'Yerlan',  'Kassymov',  'yerlan.kassymov@example.com', 'Astana IT University',                'Kazakhstan',     '+77011110006'),
('00000000-0000-0000-0000-000000000007', 'Madina',  'Zhaksylyk', 'madina.zhaksylyk@example.com','Suleyman Demirel University',         'Kazakhstan',     '+77011110007'),
('00000000-0000-0000-0000-000000000008', 'Ruslan',  'Akhmetov',  'ruslan.akhmetov@example.com', 'Karaganda Technical University',      'Kazakhstan',     '+77011110008'),
('00000000-0000-0000-0000-000000000009', 'John',    'Smith',     'john.smith@example.com',      'Massachusetts Institute of Technology','United States', '+16175550109'),
('00000000-0000-0000-0000-000000000010', 'Maria',   'Garcia',    'maria.garcia@example.com',    'University of Barcelona',             'Spain',          '+34930000110'),
('00000000-0000-0000-0000-000000000011', 'Askar',   'Omarov',    'askar.omarov@example.com',    'Nazarbayev University',               'Kazakhstan',     '+77011110011'),
('00000000-0000-0000-0000-000000000012', 'Wei',     'Li',        'wei.li@example.com',          'Tsinghua University',                 'China',          '+8610555000112');


-- authors: 1-Arman, 2-Amina, 3-Dana, 4-Timur, 9-John, 10-Maria, 11-Askar
INSERT INTO AUTHOR (author_id, orcid)
VALUES
('00000000-0000-0000-0000-000000000001', '0000-0001-1111-0001'),
('00000000-0000-0000-0000-000000000002', '0000-0001-1111-0002'),
('00000000-0000-0000-0000-000000000003', NULL),
('00000000-0000-0000-0000-000000000004', '0000-0001-1111-0004'),
('00000000-0000-0000-0000-000000000009', '0000-0001-1111-0009'),
('00000000-0000-0000-0000-000000000010', NULL),
('00000000-0000-0000-0000-000000000011', '0000-0001-1111-0011');


INSERT INTO AUTHOR_RESEARCH_AREA (author_id, area_label)
VALUES 
('00000000-0000-0000-0000-000000000001', 'Databases'),
('00000000-0000-0000-0000-000000000001', 'Machine Learning'),
('00000000-0000-0000-0000-000000000002', 'Machine Learning'),
('00000000-0000-0000-0000-000000000003', 'Natural Language Processing'),
('00000000-0000-0000-0000-000000000004', 'Databases'),
('00000000-0000-0000-0000-000000000009', 'Machine Learning'),
('00000000-0000-0000-0000-000000000009', 'Computer Vision'),
('00000000-0000-0000-0000-000000000010', 'Natural Language Processing'),
('00000000-0000-0000-0000-000000000011', 'Computer Networks');


-- reviewers: 1-Arman, 5-Aigerim, 6-Yerlan, 7-Madina, 8-Ruslan, 9-John, 10-Maria, 12-Wei
INSERT INTO REVIEWER (reviewer_id, years_experience)
VALUES
('00000000-0000-0000-0000-000000000001', 5),
('00000000-0000-0000-0000-000000000005', 7),
('00000000-0000-0000-0000-000000000006', 2),
('00000000-0000-0000-0000-000000000007', 4),
('00000000-0000-0000-0000-000000000008', 0),
('00000000-0000-0000-0000-000000000009', 10),
('00000000-0000-0000-0000-000000000010', 6),
('00000000-0000-0000-0000-000000000012', 3);


INSERT INTO REVIEWER_EXPERTISE (reviewer_id, area_label)
VALUES
('00000000-0000-0000-0000-000000000001', 'Databases'),
('00000000-0000-0000-0000-000000000005', 'Databases'),
('00000000-0000-0000-0000-000000000005', 'Machine Learning'),
('00000000-0000-0000-0000-000000000006', 'Databases'),
('00000000-0000-0000-0000-000000000007', 'Computer Vision'),
('00000000-0000-0000-0000-000000000008', 'Computer Networks'),
('00000000-0000-0000-0000-000000000009', 'Machine Learning'),
('00000000-0000-0000-0000-000000000010', 'Natural Language Processing'),
('00000000-0000-0000-0000-000000000012', 'Databases'),
('00000000-0000-0000-0000-000000000012', 'Security');


INSERT INTO CONFERENCE (conference_id, name, acronym, description, city, country, start_date, end_date,
submission_deadline, review_deadline)
VALUES
('00000000-0000-0000-0000-000000000101', 'Kazakhstan Conference on Database Systems', 
'KazDB 2026', 'Annual conference on data management, query processing and database security', 
'Astana', 'Kazakhstan', '2026-09-14', '2026-09-16', '2026-05-01', '2026-06-15'),
('00000000-0000-0000-0000-000000000102', 'Central Asian Conference on Machine Learning', 
'CAML 2026', 'Regional conference on machine learning, deep learning and computer vision', 
'Almaty', 'Kazakhstan', '2026-10-05', '2026-10-07', '2026-06-01', '2026-07-20'),
('00000000-0000-0000-0000-000000000103', 'European Workshop on Natural Language Processing', 
'EuroNLP 2026', 'Workshop on machine translation and multilingual language technologies', 
'Barcelona', 'Spain', '2026-11-10', '2026-11-12', '2026-07-01', '2026-08-30');


INSERT INTO conference_host (conference_id, host_name) 
VALUES
('00000000-0000-0000-0000-000000000101', 'Nazarbayev University'),
('00000000-0000-0000-0000-000000000101', 'Astana IT University'),
('00000000-0000-0000-0000-000000000102', 'Kazakh-British Technical University'),
('00000000-0000-0000-0000-000000000102', 'Al-Farabi Kazakh National University'),
('00000000-0000-0000-0000-000000000103', 'University of Barcelona');


INSERT INTO CONFERENCE_REVIEWER (conference_id, reviewer_id)
VALUES
-- KazDB 2026: Arman, Aigerim, Yerlan, Ruslan, Wei
('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000001'),
('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000005'),
('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000006'),
('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000008'),
('00000000-0000-0000-0000-000000000101', '00000000-0000-0000-0000-000000000012'),
-- CAML 2026: Aigerim, Madina, John, Maria
('00000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000005'),
('00000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000007'),
('00000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000009'),
('00000000-0000-0000-0000-000000000102', '00000000-0000-0000-0000-000000000010'),
-- EuroNLP 2026: Maria, Wei
('00000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000010'),
('00000000-0000-0000-0000-000000000103', '00000000-0000-0000-0000-000000000012');


-- track id has 2xx in it
INSERT INTO TRACK (track_id, conference_id, name, description, research_area, coordinator_id)
VALUES
('00000000-0000-0000-0000-000000000201', '00000000-0000-0000-0000-000000000101', 'Query Processing',
 'Query optimization, indexing and execution engines', 'Databases', '00000000-0000-0000-0000-000000000005'),
('00000000-0000-0000-0000-000000000202', '00000000-0000-0000-0000-000000000101', 'Data Management for ML',
 'Databases and data pipelines for machine learning workloads', 'Machine Learning', '00000000-0000-0000-0000-000000000001'),
('00000000-0000-0000-0000-000000000203', '00000000-0000-0000-0000-000000000101', 'Database Security',
 'Access control, privacy and secure query processing', 'Security', '00000000-0000-0000-0000-000000000012'),
('00000000-0000-0000-0000-000000000204', '00000000-0000-0000-0000-000000000102', 'Deep Learning',
 'Neural network architectures and training methods', 'Machine Learning', '00000000-0000-0000-0000-000000000009'),
('00000000-0000-0000-0000-000000000205', '00000000-0000-0000-0000-000000000102', 'Computer Vision',
 'Image recognition, detection and segmentation', 'Computer Vision', '00000000-0000-0000-0000-000000000007'),
('00000000-0000-0000-0000-000000000206', '00000000-0000-0000-0000-000000000103', 'Machine Translation',
 'Neural and multilingual machine translation', 'Natural Language Processing', '00000000-0000-0000-0000-000000000010');


-- session id has 3xx in it
INSERT INTO conference_session (session_id, conference_id, title, session_date, start_time, end_time, room_label, chair_id) 
VALUES
('00000000-0000-0000-0000-000000000301', '00000000-0000-0000-0000-000000000101', 'Query Optimization',
 '2026-09-14', '10:00', '12:00', 'Room A1', '00000000-0000-0000-0000-000000000005'),
('00000000-0000-0000-0000-000000000302', '00000000-0000-0000-0000-000000000101', 'Late-Breaking Results',
 '2026-09-15', '14:00', '15:30', 'Room B2', '00000000-0000-0000-0000-000000000001'),
('00000000-0000-0000-0000-000000000303', '00000000-0000-0000-0000-000000000102', 'Neural Networks',
 '2026-10-06', '09:30', '11:00', 'Main Hall', '00000000-0000-0000-0000-000000000009');


-- paper id has 4xx in it
INSERT INTO paper (paper_id, track_id, title, abstract, submission_date, status, session_id) 
VALUES
('00000000-0000-0000-0000-000000000401', '00000000-0000-0000-0000-000000000201', 'Adaptive Index Selection for OLTP Workloads',
 'We present an index advisor that uses machine learning to choose indexes for changing transactional workloads', '2026-04-10', 'accepted', '00000000-0000-0000-0000-000000000301'),
('00000000-0000-0000-0000-000000000402', '00000000-0000-0000-0000-000000000201', 'Cost Models for Distributed Joins',
 'A new cost model for join ordering in distributed relational databases', '2026-04-12', 'accepted', '00000000-0000-0000-0000-000000000301'),
('00000000-0000-0000-0000-000000000403', '00000000-0000-0000-0000-000000000202', 'Feature Stores Inside Relational Databases',
 'We show how Machine Learning feature stores can be implemented on top of a relational DBMS', '2026-04-15', 'accepted', NULL),
('00000000-0000-0000-0000-000000000404', '00000000-0000-0000-0000-000000000202', 'Vector Search in PostgreSQL',
 'An evaluation of approximate nearest neighbour search extensions for PostgreSQL', '2026-04-18', 'rejected', NULL),
('00000000-0000-0000-0000-000000000405', '00000000-0000-0000-0000-000000000201', 'Learned Cardinality Estimation',
 'We replace histogram-based cardinality estimation with a lightweight model', '2026-04-20', 'under review', NULL),
('00000000-0000-0000-0000-000000000411', '00000000-0000-0000-0000-000000000201', 'Compression Schemes for Column Stores',
 'A comparison of lightweight compression schemes in column-oriented storage', '2026-04-22', 'withdrawn', NULL),
('00000000-0000-0000-0000-000000000406', '00000000-0000-0000-0000-000000000204', 'Efficient Transformers for Low-Resource Data',
 'We propose a compact transformer architecture for small datasets', '2026-05-05', 'accepted', '00000000-0000-0000-0000-000000000303'),
('00000000-0000-0000-0000-000000000407', '00000000-0000-0000-0000-000000000204', 'Curriculum Learning for Small Networks',
 'A curriculum strategy that speeds up training of small neural networks', '2026-05-08', 'submitted', NULL),
('00000000-0000-0000-0000-000000000408', '00000000-0000-0000-0000-000000000205', 'Lightweight Object Detection for Drones',
 'A real-time object detector optimized for embedded drone hardware', '2026-05-10', 'rejected', NULL),
('00000000-0000-0000-0000-000000000409', '00000000-0000-0000-0000-000000000204', 'Federated Training on Mobile Devices',
 'Privacy-preserving federated training of MACHINE LEARNING models on smartphones', '2026-05-12', 'withdrawn', NULL),
('00000000-0000-0000-0000-000000000410', '00000000-0000-0000-0000-000000000205', 'Synthetic Data for Medical Imaging',
 'Generating synthetic medical images to augment small training sets', '2026-05-15', 'withdrawn', NULL);


INSERT INTO paper_author (paper_id, author_id, author_position, is_corresponding) 
VALUES
('00000000-0000-0000-0000-000000000401', '00000000-0000-0000-0000-000000000004', 1, TRUE),   
('00000000-0000-0000-0000-000000000401', '00000000-0000-0000-0000-000000000001', 2, FALSE), 
('00000000-0000-0000-0000-000000000402', '00000000-0000-0000-0000-000000000001', 1, TRUE),   
('00000000-0000-0000-0000-000000000402', '00000000-0000-0000-0000-000000000011', 2, FALSE),  
('00000000-0000-0000-0000-000000000403', '00000000-0000-0000-0000-000000000003', 1, TRUE), 
('00000000-0000-0000-0000-000000000403', '00000000-0000-0000-0000-000000000004', 2, FALSE), 
('00000000-0000-0000-0000-000000000404', '00000000-0000-0000-0000-000000000011', 1, TRUE),   
('00000000-0000-0000-0000-000000000405', '00000000-0000-0000-0000-000000000001', 1, TRUE),   
('00000000-0000-0000-0000-000000000405', '00000000-0000-0000-0000-000000000009', 2, FALSE),  
('00000000-0000-0000-0000-000000000411', '00000000-0000-0000-0000-000000000011', 1, TRUE),  
('00000000-0000-0000-0000-000000000411', '00000000-0000-0000-0000-000000000002', 2, FALSE),  
('00000000-0000-0000-0000-000000000406', '00000000-0000-0000-0000-000000000009', 1, TRUE),   
('00000000-0000-0000-0000-000000000406', '00000000-0000-0000-0000-000000000010', 2, FALSE),  
('00000000-0000-0000-0000-000000000407', '00000000-0000-0000-0000-000000000010', 1, TRUE),   
('00000000-0000-0000-0000-000000000408', '00000000-0000-0000-0000-000000000003', 1, TRUE),  
('00000000-0000-0000-0000-000000000408', '00000000-0000-0000-0000-000000000009', 2, FALSE),  
('00000000-0000-0000-0000-000000000409', '00000000-0000-0000-0000-000000000002', 1, TRUE),  
('00000000-0000-0000-0000-000000000409', '00000000-0000-0000-0000-000000000004', 2, FALSE),  
('00000000-0000-0000-0000-000000000410', '00000000-0000-0000-0000-000000000002', 1, TRUE);   


INSERT INTO paper_keyword (paper_id, keyword) 
VALUES
('00000000-0000-0000-0000-000000000401', 'indexing'),
('00000000-0000-0000-0000-000000000401', 'OLTP'),
('00000000-0000-0000-0000-000000000402', 'join ordering'),
('00000000-0000-0000-0000-000000000402', 'distributed databases'),
('00000000-0000-0000-0000-000000000403', 'feature store'),
('00000000-0000-0000-0000-000000000404', 'vector search'),
('00000000-0000-0000-0000-000000000405', 'cardinality estimation'),
('00000000-0000-0000-0000-000000000411', 'compression'),
('00000000-0000-0000-0000-000000000406', 'transformers'),
('00000000-0000-0000-0000-000000000407', 'curriculum learning'),
('00000000-0000-0000-0000-000000000408', 'object detection'),
('00000000-0000-0000-0000-000000000409', 'federated learning'),
('00000000-0000-0000-0000-000000000410', 'synthetic data');


INSERT INTO paper_version (paper_id, version_no, file_location, uploaded_at, change_note) 
VALUES
('00000000-0000-0000-0000-000000000401', 1, 'papers/401/v1.pdf', '2026-04-10 09:15:00', NULL),
('00000000-0000-0000-0000-000000000401', 2, 'papers/401/v2.pdf', '2026-07-01 18:40:00', 'Camera-ready version'),
('00000000-0000-0000-0000-000000000402', 1, 'papers/402/v1.pdf', '2026-04-12 11:00:00', NULL),
('00000000-0000-0000-0000-000000000403', 1, 'papers/403/v1.pdf', '2026-04-15 16:20:00', NULL),
('00000000-0000-0000-0000-000000000404', 1, 'papers/404/v1.pdf', '2026-04-18 10:05:00', NULL),
('00000000-0000-0000-0000-000000000405', 1, 'papers/405/v1.pdf', '2026-04-20 13:30:00', NULL),
('00000000-0000-0000-0000-000000000405', 3, 'papers/405/v3.pdf', '2026-04-28 08:45:00', 'Fixed experiments section'),
('00000000-0000-0000-0000-000000000411', 1, 'papers/411/v1.pdf', '2026-04-22 12:00:00', NULL),
('00000000-0000-0000-0000-000000000406', 1, 'papers/406/v1.pdf', '2026-05-05 14:10:00', NULL),
('00000000-0000-0000-0000-000000000406', 2, 'papers/406/v2.pdf', '2026-08-10 20:00:00', 'Camera-ready version'),
('00000000-0000-0000-0000-000000000407', 1, 'papers/407/v1.pdf', '2026-05-08 09:00:00', NULL),
('00000000-0000-0000-0000-000000000408', 1, 'papers/408/v1.pdf', '2026-05-10 17:25:00', NULL),
('00000000-0000-0000-0000-000000000409', 1, 'papers/409/v1.pdf', '2026-05-12 15:50:00', NULL),
('00000000-0000-0000-0000-000000000410', 1, 'papers/410/v1.pdf', '2026-05-15 10:30:00', NULL);


-- review id has 5xx in it
INSERT INTO review (review_id, paper_id, reviewer_id, overall_score, recommendation, comments_for_authors, confidential_comments, review_submission_date) 
VALUES
('00000000-0000-0000-0000-000000000501', '00000000-0000-0000-0000-000000000401', '00000000-0000-0000-0000-000000000005', 5, 'accept', 'Strong experimental evaluation', NULL, '2026-06-01'),
('00000000-0000-0000-0000-000000000502', '00000000-0000-0000-0000-000000000401', '00000000-0000-0000-0000-000000000012', 4, 'accept', 'Clear motivation, minor typos', NULL, '2026-06-03'),
('00000000-0000-0000-0000-000000000503', '00000000-0000-0000-0000-000000000401', '00000000-0000-0000-0000-000000000006', 4, 'accept', 'Good paper', 'Could be a best paper candidate', '2026-06-05'),
('00000000-0000-0000-0000-000000000504', '00000000-0000-0000-0000-000000000402', '00000000-0000-0000-0000-000000000005', 4, 'accept', 'Solid cost model', NULL, '2026-06-02'),
('00000000-0000-0000-0000-000000000505', '00000000-0000-0000-0000-000000000402', '00000000-0000-0000-0000-000000000012', 5, 'accept', 'Well written', NULL, '2026-06-04'),
('00000000-0000-0000-0000-000000000506', '00000000-0000-0000-0000-000000000403', '00000000-0000-0000-0000-000000000005', 4, 'accept', 'Useful practical contribution', NULL, '2026-06-06'),
('00000000-0000-0000-0000-000000000507', '00000000-0000-0000-0000-000000000403', '00000000-0000-0000-0000-000000000001', 4, 'accept', 'Please add a scalability experiment', NULL, '2026-06-07'),
('00000000-0000-0000-0000-000000000508', '00000000-0000-0000-0000-000000000404', '00000000-0000-0000-0000-000000000005', 2, 'reject', 'Limited novelty', NULL, '2026-06-08'),
('00000000-0000-0000-0000-000000000509', '00000000-0000-0000-0000-000000000404', '00000000-0000-0000-0000-000000000006', 2, 'reject', 'Evaluation is too small', NULL, '2026-06-09'),
('00000000-0000-0000-0000-000000000510', '00000000-0000-0000-0000-000000000405', '00000000-0000-0000-0000-000000000012', 3, 'accept', 'Promising, needs more baselines', NULL, '2026-06-10'),
('00000000-0000-0000-0000-000000000511', '00000000-0000-0000-0000-000000000411', '00000000-0000-0000-0000-000000000012', 2, 'reject', 'Results are not reproducible', NULL, '2026-06-11'),
('00000000-0000-0000-0000-000000000512', '00000000-0000-0000-0000-000000000406', '00000000-0000-0000-0000-000000000005', 5, 'accept', 'Excellent results on small datasets', NULL, '2026-07-10'),
('00000000-0000-0000-0000-000000000513', '00000000-0000-0000-0000-000000000406', '00000000-0000-0000-0000-000000000007', 4, 'accept', 'Good architecture study', NULL, '2026-07-12'),
('00000000-0000-0000-0000-000000000514', '00000000-0000-0000-0000-000000000408', '00000000-0000-0000-0000-000000000007', 2, 'reject', 'Comparison with baselines is missing', NULL, '2026-07-13'),
('00000000-0000-0000-0000-000000000515', '00000000-0000-0000-0000-000000000408', '00000000-0000-0000-0000-000000000010', 1, 'reject', 'Out of scope for this track', 'Possible duplicate submission', '2026-07-14'),
('00000000-0000-0000-0000-000000000516', '00000000-0000-0000-0000-000000000409', '00000000-0000-0000-0000-000000000005', 3, 'reject', 'Privacy analysis is incomplete', NULL, '2026-07-15');
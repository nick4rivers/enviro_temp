-- need to add logger_serial

INSERT INTO deployments (
    deployment_id,
    site_id,
    deployment_date,
    deployment_time,
    deployment_description,
    retrieval_status_id,
    retrieval_date,
    retrieval_time,
    retrieval_description
    ) VALUES (
    1, 1,
    '2005-01-01', '17:00:00',
    'Near a large beaver dam',
    1,
    '2005-02-25', '12:00:00',
    'Near a large beaver dam'
    );


INSERT INTO deployments (
    deployment_id, site_id,
    deployment_date, deployment_time,
    deployment_description,
    retrieval_status_id,
    retrieval_date, retrieval_time,
    retrieval_description
    ) VALUES (
    2, 1,
    '2006-03-21', '17:00:00',
    'Near a large beaver dam',
    1,
    '2006-06-25', '12:00:00',
    'Near a large beaver dam'
    );

INSERT INTO deployments (
    deployment_id, site_id,
    deployment_date, deployment_time,
    deployment_description,
    retrieval_status_id,
    retrieval_date, retrieval_time,
    retrieval_description
    ) VALUES (
    3, 1,
    '2007-03-21', '17:00:00',
    'Pick me up please',
    NULL, NULL, NULL, NULL
    );

INSERT INTO deployments (
    deployment_id, site_id,
    deployment_date, deployment_time,
    deployment_description,
    retrieval_status_id,
    retrieval_date, retrieval_time,
    retrieval_description
    ) VALUES (
    4, 3,
    '2006-03-21', '17:00:00',
    'Near Stuff',
    2,
    '2006-06-25', '12:00:00',
    'Near a large beaver dam'
    );

INSERT INTO deployments (
    deployment_id, site_id,
    deployment_date, deployment_time,
    deployment_description,
    retrieval_status_id,
    retrieval_date, retrieval_time,
    retrieval_description
    ) VALUES (
    5, 3,
    '2010-03-21', '17:00:00',
    'Yeah get the logger',
    2,
    '2011-06-25', '12:00:00',
    'Logger - logger'
    );

INSERT INTO deployments (
    deployment_id, site_id,
    deployment_date, deployment_time,
    deployment_description,
    retrieval_status_id,
    retrieval_date, retrieval_time,
    retrieval_description
    ) VALUES (
    6, 2,
    '2010-03-21', '17:00:00',
    'Remember to pick me up',
    NULL, NULL, NULL, NULL
    );
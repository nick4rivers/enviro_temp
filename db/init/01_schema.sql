CREATE extension IF NOT EXISTS postgis;

CREATE TABLE projects
(
    project_id   INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    project_name VARCHAR(255) UNIQUE NOT NULL,
    project_description  TEXT,
    metadata JSON,
    created_date TIMESTAMPTZ      NOT NULL DEFAULT now(),
    updated_date TIMESTAMPTZ      NOT NULL DEFAULT now(),

    CONSTRAINT ck_projects_project_name CHECK (length(project_name) > 0)
);

CREATE TABLE site_status
(
    site_status_id   INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    site_status_name VARCHAR(255) UNIQUE NOT NULL,
    site_status_description VARCHAR(255)
);

CREATE TABLE sites
(
    site_id      INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    project_id   INT              NOT NULL,
    site_name    VARCHAR(255)     NOT NULL,
    stream_name  VARCHAR(255)     NOT NULL,
    site_description  TEXT,
    site_status_id    INT         NOT NULL,
    geom         Geography(Point) NOT NULL,
    metadata JSON,
    created_date TIMESTAMPTZ      NOT NULL DEFAULT now(),
    updated_date TIMESTAMPTZ      NOT NULL DEFAULT now(),

    CONSTRAINT ck_sites_site_name CHECK (length(site_name) > 0),
    CONSTRAINT fk_sites_project_id FOREIGN KEY (project_id) references projects (project_id),
    CONSTRAINT fk_sites_site_status_id FOREIGN KEY (site_status_id) references site_status (site_status_id)
);

CREATE UNIQUE INDEX fx_sites_project_id ON sites (project_id, site_name);
CREATE INDEX gx_sites_geom ON sites  USING GIST (geom);


-------------------------------------------------------------------------------

-- TODO: consider making this list of lookup values part of the Qt dialog?
CREATE TABLE retrieval_status
(
    retrieval_status_id          INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    retrieval_status_name        VARCHAR(255) NOT NULL,
    retrieval_status_description TEXT,
    created_date                 TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_date                 TIMESTAMPTZ  NOT NULL DEFAULT now()
);
-------------------------------------------------------------------------------

-- # TODO: consider adding a logger_serial table to actually track individual loggers?
CREATE TABLE deployments
(
    deployment_id          INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    site_id                INT         NOT NULL,
    logger_serial          TEXT        NOT NULL,
    deployment_date        DATE        NOT NULL,
    deployment_time        TIME        NOT NULL,
    deployment_description TEXT        NOT NULL,
    retrieval_status_id    INT,
    retrieval_date         DATE,
    retrieval_time         TIME,
    retrieval_description  TEXT,
    metadata JSON,
    created_date           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_date           TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_deployments_project_name CHECK (length(project_name) > 0)

    CONSTRAINT fk_deployments_site_id FOREIGN KEY (site_id) REFERENCES sites (site_id) ON DELETE CASCADE,
    CONSTRAINT fk_deployments_retrieval_status_id FOREIGN KEY (retrieval_status_id) REFERENCES retrieval_status (retrieval_status_id)
);

CREATE INDEX fx_deployments_site_id ON deployments (site_id);
CREATE INDEX fx_deployments_retrieval_status_id ON deployments(retrieval_status_id);

-------------------------------------------------------------------------------

CREATE TABLE measurements
(
    measurement_id        SERIAL PRIMARY KEY,
    deployment_id         INT         NOT NULL,
    measurement_date_time TIMESTAMPTZ NOT NULL,
    temperature           NUMERIC     NOT NULL,
    created_date          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_date          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_measurements_deployment_id FOREIGN KEY (deployment_id) REFERENCES deployments (deployment_id) ON DELETE CASCADE
);

CREATE INDEX fx_measurements_deployment_id ON measurements (deployment_id);

-------------------------------------------------------------------------------
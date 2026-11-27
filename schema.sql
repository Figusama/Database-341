DROP TABLE IF EXISTS REVIEW, PAPER_VERSION, PAPER_AUTHOR, PAPER_KEYWORD, PAPER,
  CONFERENCE_SESSION, TRACK, CONFERENCE_REVIEWER, CONFERENCE_HOST, CONFERENCE,
  REVIEWER_EXPERTISE, REVIEWER, AUTHOR_RESEARCH_AREA, AUTHOR, APP_USER CASCADE;


CREATE TABLE APP_USER(
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
    given_name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    affiliation VARCHAR(255) NOT NULL,
    country VARCHAR(57) NOT NULL,
    phone_number VARCHAR(16) NOT NULL
);

CREATE TABLE AUTHOR(
    author_id UUID NOT NULL REFERENCES APP_USER(user_id) ON DELETE CASCADE,
    orcid VARCHAR(20) NULL,
    PRIMARY KEY(author_id)
);

CREATE TABLE AUTHOR_RESEARCH_AREA(
    author_id UUID NOT NULL REFERENCES AUTHOR(author_id) ON DELETE CASCADE,
    area_label VARCHAR(100) NOT NULL,
    PRIMARY KEY(author_id, area_label)
);

CREATE TABLE REVIEWER(
    reviewer_id UUID NOT NULL REFERENCES APP_USER(user_id) ON DELETE CASCADE,
    years_experience INT NOT NULL CHECK (years_experience >= 0),
    PRIMARY KEY(reviewer_id)
);

CREATE TABLE REVIEWER_EXPERTISE(
    reviewer_id UUID NOT NULL REFERENCES REVIEWER(reviewer_id) ON DELETE CASCADE,
    area_label VARCHAR(100) NOT NULL,
    PRIMARY KEY(reviewer_id, area_label)
);

CREATE TABLE CONFERENCE(
    conference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    acronym VARCHAR(50) NOT NULL,
    description VARCHAR(400) NOT NULL, 
    city VARCHAR(50) NOT NULL,
    country VARCHAR(57) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL CHECK (end_date >= start_date),
    submission_deadline DATE NOT NULL,
    review_deadline DATE NOT NULL
);

CREATE TABLE CONFERENCE_HOST(
    conference_id UUID NOT NULL REFERENCES CONFERENCE(conference_id),
    host_name VARCHAR(200) NOT NULL,
    PRIMARY KEY(conference_id, host_name)
);

CREATE TABLE CONFERENCE_REVIEWER(
    conference_id UUID NOT NULL REFERENCES CONFERENCE(conference_id),
    reviewer_id UUID NOT NULL REFERENCES REVIEWER(reviewer_id) ON DELETE CASCADE,
    PRIMARY KEY(conference_id, reviewer_id)
);

CREATE TABLE TRACK(
    track_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conference_id UUID NOT NULL REFERENCES CONFERENCE(conference_id),
    name VARCHAR(100) NOT NULL,
    description VARCHAR(400) NOT NULL,
    research_area VARCHAR(100) NOT NULL,
    coordinator_id UUID NOT NULL REFERENCES REVIEWER(reviewer_id)
);

CREATE TABLE CONFERENCE_SESSION(
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conference_id UUID NOT NULL REFERENCES CONFERENCE(conference_id),
    title VARCHAR(100) NOT NULL,
    session_date DATE NOT NULL, 
    start_time TIME NOT NULL,
    end_time TIME NOT NULL CHECK (end_time > start_time),
    room_label VARCHAR(50) NOT NULL,
    chair_id UUID NOT NULL REFERENCES REVIEWER(reviewer_id)
);

CREATE TABLE PAPER(
    paper_id UUID DEFAULT gen_random_uuid(),
    track_id UUID NOT NULL REFERENCES TRACK(track_id),
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    submission_date DATE NOT NULL,
    status VARCHAR(12) NOT NULL CHECK(status IN ('submitted', 'under review', 'accepted', 'rejected', 'withdrawn')),
    session_id UUID REFERENCES CONFERENCE_SESSION(session_id),
    PRIMARY KEY(paper_id)
);

CREATE TABLE PAPER_KEYWORD(
    paper_id UUID NOT NULL REFERENCES PAPER(paper_id) ON DELETE CASCADE,
    keyword VARCHAR(100) NOT NULL,
    PRIMARY KEY(paper_id, keyword)
);

CREATE TABLE PAPER_AUTHOR(
    paper_id UUID NOT NULL REFERENCES PAPER(paper_id) ON DELETE CASCADE,
    author_id UUID NOT NULL REFERENCES AUTHOR(author_id),
    author_position INTEGER NOT NULL CHECK(author_position > 0),
    is_corresponding BOOLEAN NOT NULL,
    PRIMARY KEY(paper_id, author_id),
    UNIQUE(paper_id, author_position)
);

CREATE TABLE PAPER_VERSION(
    paper_id UUID NOT NULL REFERENCES PAPER(paper_id) ON DELETE CASCADE,
    version_no INTEGER NOT NULL CHECK(version_no > 0), 
    file_location TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL,
    change_note TEXT,
    PRIMARY KEY(paper_id, version_no)
);

CREATE TABLE REVIEW(
    review_id UUID NOT NULL DEFAULT gen_random_uuid(),
    paper_id UUID NOT NULL REFERENCES PAPER(paper_id) ON DELETE CASCADE,
    reviewer_id UUID NOT NULL REFERENCES REVIEWER(reviewer_id),
    overall_score INTEGER NOT NULL CHECK(overall_score BETWEEN 1 AND 5), 
    recommendation VARCHAR(6) NOT NULL CHECK(recommendation IN ('accept', 'reject')),
    comments_for_authors TEXT NOT NULL,
    confidential_comments TEXT,
    review_submission_date DATE NOT NULL,
    PRIMARY KEY(review_id),
    UNIQUE(paper_id, reviewer_id)
);




CREATE UNIQUE INDEX one_corresponding_per_paper
  ON PAPER_AUTHOR(paper_id) WHERE is_corresponding;

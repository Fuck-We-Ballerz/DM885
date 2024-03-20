CREATE TABLE IF NOT EXISTS assignment_config (
  id INT GENERATED ALWAYS AS IDENTITY,
  max_ram INT NOT NULL,
  max_cpu FLOAT NOT NULL,
  max_time INTERVAL NOT NULL,
  max_submission INT NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS assignment (
  id INT GENERATED ALWAYS AS IDENTITY,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  is_visible BOOLEAN NOT NULL,
  docker_image VARCHAR(64) NOT NULL,
  config_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(config_id) REFERENCES assignment_config(id)
);

CREATE TABLE IF NOT EXISTS student (
  id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(64) NOT NULL,
  password VARCHAR(64) NOT NULL,
  username VARCHAR(64) NOT NULL,
  open_assignment_count INT DEFAULT 0 NOT NULL,
  PRIMARY KEY(id),
  UNIQUE(username)
);

CREATE TABLE IF NOT EXISTS teacher (
  id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(64) NOT NULL,
  password VARCHAR(64) NOT NULL,
  username VARCHAR(64) NOT NULL,
  is_paused BOOLEAN DEFAULT FALSE NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS admin (
  id INT GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(64) NOT NULL,
  password VARCHAR(64) NOT NULL,
  username VARCHAR(64) NOT NULL,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS submission (
  id INT GENERATED ALWAYS AS IDENTITY,
  grade VARCHAR(64) DEFAULT 'Not graded' NOT NULL,
  status VARCHAR(64) DEFAULT 'Pending' NOT NULL,
  submission BYTEA,
  submission_std VARCHAR(64) DEFAULT '' NOT NULL,
  submission_err VARCHAR(64) DEFAULT '' NOT NULL,
  submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  assignment_id INT,
  student_id INT,
  FOREIGN KEY(assignment_id) REFERENCES assignment(id),
  FOREIGN KEY(student_id) REFERENCES student(id),
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS student_to_assignment (
  assignment_id INT,
  student_id INT,
  FOREIGN KEY(assignment_id) REFERENCES assignment(id),
  FOREIGN KEY(student_id) REFERENCES student(id),
  PRIMARY KEY(assignment_id, student_id)
);

CREATE TABLE IF NOT EXISTS teacher_to_assignment (
  assignment_id INT,
  teacher_id INT,
  FOREIGN KEY(assignment_id) REFERENCES assignment(id),
  FOREIGN KEY(teacher_id) REFERENCES teacher(id),
  PRIMARY KEY(assignment_id, teacher_id)
);

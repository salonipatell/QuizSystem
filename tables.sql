-- create_tables.sql
--database 
create database quizdata
-- Table for teachers
CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teachername VARCHAR(100) NOT NULL,
    address VARCHAR(100) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Table for students
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    studentname VARCHAR(100) NOT NULL,
    highestqualification VARCHAR(100),
    mobileno VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Table for parents
CREATE TABLE parents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parentname VARCHAR(100) NOT NULL,
    mobileno VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(100) NOT NULL,
    child_name INT,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (child_name) REFERENCES students(id)
);

-- Table for quiz questions
CREATE TABLE quizquestions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    option1 VARCHAR(255) NOT NULL,
    option2 VARCHAR(255) NOT NULL,
    option3 VARCHAR(255) NOT NULL,
    option4 VARCHAR(255) NOT NULL,
    correct_option VARCHAR(255) NOT NULL
);


-- Table for quizscores
CREATE TABLE quizscores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);




--quizquestions
INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('What is Python?', 'A type of snake', 'A programming language', 'A mathematical concept', 'A city in Europe', 'A programming language');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('Which keyword is used to define a function in Python?', 'method', 'def', 'class', 'function', 'def');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('Which data type is used to store a sequence of characters in Python?', 'string', 'char', 'text', 'str', 'str');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('What is the output of the following code: print(2 + 3 * 4)', '14', '20', '10', '23', '14');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('Which loop is used to iterate over a sequence in Python?', 'for', 'while', 'loop', 'do-while', 'for');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('Which Python library is commonly used for data analysis and manipulation?', 'matplotlib', 'numpy', 'pandas', 'scikit-learn', 'pandas');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('What is the result of this expression? bool(5 < 3)', 'True', 'False', 'Error', 'None', 'False');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('What does the built-in function len() return?', 'The length of a string', 'The logarithm of a number', 'The square root of a number', 'The value of pi', 'The length of a string');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('Which Python keyword is used to define a conditional statement?', 'case', 'select', 'switch', 'if', 'if');

INSERT INTO quizquestions (question_text, option1, option2, option3, option4, correct_option)
VALUES ('What is the correct way to create a list in Python?', '[1, 2, 3]', '(1, 2, 3)', '{1, 2, 3}', '1, 2, 3', '[1, 2, 3]');



-- Drop existing tables if they exist
DROP TABLE IF EXISTS Documents;
DROP TABLE IF EXISTS Notebooks;
DROP TABLE IF EXISTS Users;

-- Create Users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Notebooks table
CREATE TABLE Notebooks (
    notebook_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Documents table
CREATE TABLE Documents (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    notebook_id INT NOT NULL,
    content TEXT NOT NULL,
    vectorized_content BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notebook_id) REFERENCES Notebooks(notebook_id) ON DELETE CASCADE
);

-- Create stored procedure to add a new user
DELIMITER //
CREATE PROCEDURE create_user(IN new_username VARCHAR(255))
BEGIN
    INSERT INTO Users (username) VALUES (new_username);
END //
DELIMITER ;

-- Create stored procedure to add a new notebook
DELIMITER //
CREATE PROCEDURE create_notebook(IN user_id INT, IN notebook_title VARCHAR(255))
BEGIN
    INSERT INTO Notebooks (user_id, title) VALUES (user_id, notebook_title);
END //
DELIMITER ;

-- Create stored procedure to add a document to a notebook
DELIMITER //
CREATE PROCEDURE add_document(IN notebook_id INT, IN document_content TEXT, IN vectorized_content BLOB)
BEGIN
    INSERT INTO Documents (notebook_id, content, vectorized_content) VALUES (notebook_id, document_content, vectorized_content);
END //
DELIMITER ;
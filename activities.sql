-- Create activities table
CREATE TABLE IF NOT EXISTS activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert example records
INSERT INTO activities (name, description) VALUES
('Read Notes', 'User reads notes from the database'),
('Create Note', 'User creates a new note'),
('Tag Management', 'User adds or edits tags for notes');

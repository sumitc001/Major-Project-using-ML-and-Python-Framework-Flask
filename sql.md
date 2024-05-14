![image](https://github.com/csubham2370/Major-Project-using-ML-and-Python-Framework-Flask/assets/144363196/1b433e1b-dcc0-44c5-8773-6f3445c9a627)

Certainly! Here are some common SQL operations you can perform on a table:

1. **Create Table:**
   - To create a new table, use the `CREATE TABLE` statement. Specify the table name and its columns along with their data types.
   - Example:
     ```sql
     CREATE TABLE users (
         id INT PRIMARY KEY,
         name VARCHAR(50),
         email VARCHAR(100),
         password VARCHAR(100)
     );
     ```

2. **Insert Records:**
   - Use the `INSERT INTO` statement to add data to the table.
   - Example:
     ```sql
     INSERT INTO users (id, name, email, password)
     VALUES (1, 'Alice', 'alice@example.com', 'hashed_password');
     ```

3. **Update Records:**
   - Modify existing data using the `UPDATE` statement.
   - Example:
     ```sql
     UPDATE users SET email = 'new_email@example.com' WHERE id = 1;
     ```

4. **Delete Records:**
   - Remove data using the `DELETE FROM` statement.
   - Example:
     ```sql
     DELETE FROM users WHERE id = 1;
     ```

5. **Retrieve Data:**
   - Use the `SELECT` statement to retrieve data from the table.
   - Example:
     ```sql
     SELECT * FROM users WHERE name = 'Alice';
     ```

6. **Alter Table (Add Column):**
   - To add a new column to an existing table, use the `ALTER TABLE` statement.
   - Example:
     ```sql
     ALTER TABLE users ADD last_login TIMESTAMP;
     ```

Remember to adjust the table name ("users") and column names according to your specific use case. If you have any more questions, feel free to ask! 😊


## Download mysql or mysql workbench
##  create this table
![image](https://github.com/csubham2370/Major-Project-using-ML-and-Python-Framework-Flask/assets/144363196/1b433e1b-dcc0-44c5-8773-6f3445c9a627)

# Database Query:
* How to create a database?
* Ans: CREATE SCHEMA `flask` ;
* How to create a table?
* Ans: CREATE TABLE `flask2`.`users` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `reset_token` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));
* #How to display the data in the table in DB?
* Ans: SELECT * FROM flask.users;
* How to delete a data in the data base?
* Ans: DELETE FROM `flask`.`users` WHERE (`id` = '1') and (`email` = 'subho4321@gmail.com');


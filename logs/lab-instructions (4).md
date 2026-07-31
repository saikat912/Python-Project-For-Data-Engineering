::page{title="Hands-on Lab: Improving Performance of Slow Queries in MySQL"}

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/module%201/images/SN_web_lightmode.png" width="300">


**Estimated time needed:** 45 minutes

In this lab, you will learn how to improve the performance of your slow queries in MySQL, which can be particularly helpful with large databases.

::page{title="Objectives"}

After completing this lab, you will be able to:

1. Use the `EXPLAIN` statement to check the performance of your query
2. Add indexes to improve the performance of your query
3. Apply other best practices such as using the `UNION ALL` clause to improve query performance

::page{title="Software Used in this Lab"}

In this lab, you will use [MySQL](https://www.mysql.com/)</a>. MySQL is a Relational Database Management System (RDBMS) designed to efficiently store, manipulate, and retrieve data.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/mysql.png" width="100" height="100">

To complete this lab, you will utilize the MySQL relational database service available as part of the IBM Skills Network Labs (SN Labs) Cloud IDE. SN Labs is a virtual lab environment used in this course.

::page{title="Database Used in this Lab"}

The Employees database used in this lab comes from the following source: [https://dev.mysql.com/doc/employee/en/](https://dev.mysql.com/doc/employee/en/) under the [CC BY-SA 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/).

The following entity relationship diagram (ERD) shows the schema of the Employees database:

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/employees-schema.png" height="400">

The first row of each table is the table name, the rows with keys next to them indicate the primary keys, and the remaining rows are additional attributes.

::page{title="Exercise 1: Load the Database"}

Let's begin by retrieving the database and loading it so that it can be used.

1. In the menu bar, select `Terminal > New Terminal`. This will open the Terminal.

    To download the zip file containing the database, copy and paste the following into the Terminal:

    ```bash
    wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/datasets/employeesdb.zip
    ```
    

    ![Download Database](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/a-download_database.png)

2. Next, we'll need to unzip its contents. We can do that with the following command:

    ```bash
    unzip employeesdb.zip
    ```
    

    ![Unzipping the Downloaded Database](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/a-unzip_database.png)

3. Now, let's change directories so that we're able to access the files in the newly created **employeesdb** folder.

    ```bash
    cd employeesdb
    ```
    

    Check the line next to **theia@theiadocker**. If it reads **/home/project/employeesdb**, then you have successfully changed directories!

    ![Changing Directories](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/a-change_directories.png)

4. Start the MySQL service session  using the `Start MySQL in IDE  button` directive.
	

(::openDatabase{db="MySQL" start="false"}) 

    
	
5. On the launching page, click on the **Create** button.


![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/0fIjtcRkAkn5aEwr-GfvyQ/k2-1.png)

6. With your password handy, we can now import the data. You can do this by entering the following into the Terminal:

    ```bash
    mysql --host=mysql --port=3306 --user=root --password -t < employees.sql
    ```
When prompted, enter the password that was displayed under the **Connection Information** section when MySQL started up.

> Please note, you won\'t be able to see your password when typing it in. Not to worry, this is expected!!


7. Your data will now load. This may take a minute or so.

    When you've finished loading the data, you'll see the following:

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/Dvc2ViiLfT5haE01N4fYug/A6.PNG)

This means that your data has been imported.

8. To enter the MySQL command-line interface, return to your MySQL tab and select **MySQL CLI**.

	
	![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/PY0u8YRYSB9F69VA4r8uBg/k2-4.png)

9. Recall that the name of the database that we're using is **Employees**. To access it, we can use this command:

    ```bash
    use employees
    ```
    

    ![Use Employees Database](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/a-database_changed.png)

10. Let's see which tables are available in this database:

    ```bash
    show tables;
    ```
    

    ![Show Tables in Employees Database](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/a-show_tables.png)

    In this database, there are 8 tables, which we can confirm with the database's ERD.

Now that your database is all set up, let's take a look at how we can check a query's performance!

::page{title="Exercise 2: Check Your Query's Performance with EXPLAIN"}

The `EXPLAIN` statement, which provides information about how MySQL executes your statement, will offer you insight about the number of rows your query is planning on looking through. This statement can be helpful when your query is running slow. For example, is it running slow because it's scanning the entire table each time?

1. Let's start with selecting all the data from the **employees** table:

    ```SQL
    SELECT * FROM employees;
    ```
    

    ![Select All Output](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/b-select_all_output.png)

    As you can see, all 300,024 rows were loaded, taking about 0.34 seconds.

2. We can use `EXPLAIN` to see how many rows were scanned:

    ```SQL
    EXPLAIN SELECT * FROM employees;
    ```
    

    ![EXPLAIN Select All Output](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/b-explain_select_all_output.png)

    Notice how `EXPLAIN` shows that it is examining 298,980 rows, almost the entire table! With a larger table, this could result in the query running slowly.

So, how can we make this query faster? That's where indexes come in!

::page{title="Exercise 3: Add an Index to Your Table"}

1. To begin, let's take at the existing indexes. We can do that by entering the following command:

    ```SQL
    SHOW INDEX FROM employees;
    ```
    

    ![Primary Key Indexes](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-show_indexes_primarykey.png)

    Remember that indexes for primary keys are created automatically, as we can see above. An index has already been created for the primary key, **emp_no**. If we think about this, this makes sense because each employee number is unique to the employee, with no NULL values.

2. Now, let's say we wanted to see all the information about employees who were hired on or after January 1, 2000. We can do that with the query:

    ```SQL
    SELECT * FROM employees WHERE hire_date >= '2000-01-01';
    ```
    

    ![Select All Columns With Hire Date Before January 1, 2000](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-sample_hiredate.png)

    As we can see, the 13 rows returned took about 0.17 seconds to execute. That may not seem like a long time with this table, but keep in mind that with larger tables, this time can vary greatly.

3. With the `EXPLAIN` statement, we can check how many rows this query is scanning:

    ```SQL
    EXPLAIN SELECT * FROM employees WHERE hire_date >= '2000-01-01';
    ```
    

    ![EXPLAIN Select All Columns With Hire Date Before January 1, 2000](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-sample_explain_hiredate.png)

    This query results in a scan of 299,423 rows, which is nearly the entire table!

    By adding an index to the **hire_date** column, we'll be able to reduce the query's need to search through every entry of the table, instead only searching through what it needs.

4. You can add an index with the following:

    ``` SQL
    CREATE INDEX hire_date_index ON employees(hire_date);
    ```
    

    The `CREATE INDEX` command creates an index called **hire_date_index** on the table **employees** on column **hire_date**.

    ![Create an Index on Hire Date](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-create_hiredate_index.png)

5. To check your index, you can use the `SHOW INDEX` command:

    ```SQL
    SHOW INDEX FROM employees;
    ```
    

    Now you can see that we have both the **emp_no** index and **hire_date** index.

    ![Show Primary and New Hire Date Indexes](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-show_index_primarykey_and_hiredateindex.png)

    With the index added,

6. Once more, let's select all the employees who were hired on or after January 1, 2000.

    ```SQL
    SELECT * FROM employees WHERE hire_date >= '2000-01-01';
    ```
    

    ![Select All Columns With Hire Date Before January 1, 2000 With Index](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-sample_hiredate_with_index.png)

    The difference is quite evident! Rather than taking about 0.17 seconds to execute the query, it takes 0.00 seconds—almost no time at all.

7. We can use the `EXPLAIN` statement to see how many rows were scanned:

    ```SQL
    EXPLAIN SELECT * FROM employees WHERE hire_date >= '2000-01-01';
    ```
    

    ![EXPLAIN Select All Columns With Hire Date Before January 1, 2000 with Index](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-sample_explain_hiredate_with_index.png)

    Under **rows**, we can see that only the necessary 13 columns were scanned, leading to the improved performance.

    Under **Extra**, you can also see that it has been explicitly stated that the index was used, that index being **hire_date_index** based on the **possible_keys** column.

Now, if you want to remove the index, enter the following into the Terminal:

```SQL
DROP INDEX hire_date_index ON employees;
```

This will remove the **hire_date_index** on the **employees** table. You can check with the `SHOW INDEX` command to confirm:

![Drop Hire Date Index and Show Current Indexes in Employee Table](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/c-drop_and_show_index.png)

::page{title="Exercise 4: Use an UNION ALL Clause"}

Sometimes, you might want to run a query using the `OR` operator with `LIKE` statements. In this case, using a `UNION ALL` clause can improve the speed of your query, particularly if the columns on both sides of the `OR` operator are indexed.

1. To start, let's run this query:

    ```SQL
    SELECT * FROM employees WHERE first_name LIKE 'C%' OR last_name LIKE 'C%';
    ```
    

    ![Sample OR Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-sample_or_query.png)

    This query searches for first names or last names that start with "C". It returned 28,970 rows, taking about 0.20 seconds.

2. Check using the `EXPLAIN` command to see how many rows are being scanned!

    <details>
    <summary>Hint (Click Here)</summary>

    Review how we used the `EXPLAIN` statement in Exercise A and apply it to the above query.

    </details>

    <details>
    <summary>Solution (Click Here)</summary>

    Your statement should look like the following:

    ```SQL
    EXPLAIN SELECT * FROM employees WHERE first_name LIKE 'C%' OR last_name LIKE 'C%';
    ```
    

    ![EXPLAIN Sample OR Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-explain_sample_or_query.png)
    </details>

    Once more, we can see that almost all the rows are being scanned, so let's add indexes to both the **first_name** and **last_name** columns.

3. Try adding an index to both the **first_name** and **last_name** columns.

    <details>
    <summary>Hint (Click Here)</summary>

    Consider how we created an index in Exercise B. How can you apply this to a different column?
    </details>

    <details>
    <summary>Solution (Click Here)</summary>

    You can add the indexes with the following:
    ``` SQL
    CREATE INDEX first_name_index ON employees(first_name);
    CREATE INDEX last_name_index ON employees(last_name);
    ```
    

    Please note, the name of your indexes (**first_name_index** and **last_name_index**) can be named differently.

    You can also check to see if your indexes have been added with the `SHOW INDEX` command:

    ![Add an Index to First Name and Last Name and Show Current Indexes](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-add_indexes_show_index.png)
    </details>

4. Great! With your indexes now in place, we can re-run the query:

    ```SQL
    SELECT * FROM employees WHERE first_name LIKE 'C%' OR last_name LIKE 'C%';
    ```
    

    ![Re-running Sample OR Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-sample_or_query_rerun.png)

    Let's also see how many rows are being scanned:

    ```SQL
    EXPLAIN SELECT * FROM employees WHERE first_name LIKE 'C%' OR last_name LIKE 'C%';
    ```
    

    ![EXPLAIN Re-running Sample OR Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-explain_sample_or_query_rerun.png)

    With indexes, the query still scans all the rows.

5. Let's use the `UNION ALL` clause to improve the performance of this query.

    We can do this with the following:

    ```SQL
    SELECT * FROM employees WHERE first_name LIKE 'C%' UNION ALL SELECT * FROM employees WHERE last_name LIKE 'C%';
    ```
    

    ![Sample UNION ALL Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-sample_union_all_query.png)

    As we can see, this query only takes 0.11 seconds to execute, running faster than when we used the `OR` operator.

    Using the `EXPLAIN` statement, we can see why that might be:

    ![Sample EXPLAIN UNION ALL Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-explain_sample_union_all_query.png)

    As the `EXPLAIN` statement reveals, there were two `SELECT` operations performed, with the total number of rows scanned sitting at 54,790. This is less than the original query that scanned the entire table and, as a result, the query performs faster.

Please note, if you choose to perform a leading wildcard search with an index, the entire table will still be scanned. You can see this yourself with the following query:

```SQL
SELECT * FROM employees WHERE first_name LIKE '%C';
```

With this query, we want to find all the employees whose first names end with "C".

When checking with the `EXPLAIN` and `SHOW INDEX` statements, we can see that although we have an index on **first_name**, the index is not used and results in a search of the entire table.

Under the `EXPLAIN` statement's **possible_keys** column, we can see that this index has not been used as the entry is NULL.

![Sample Leading Wildcard Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-sample_leading_wildcard_query.png)

On the other hand, indexes do work with trailing wildcards, as seen with the following query that finds all employees whose first names begin with "C":

```SQL
SELECT * FROM employees WHERE first_name LIKE 'C%';
```

![Sample Trailing Wildcard Query](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/d-sample_trailing_wildcard_query.png)

Under the `EXPLAIN` statement's **possible_keys** and **Extra** columns, we can see that the **first_name_index** is used. With only 20,622 rows scanned, the query performs better.

::page{title="Exercise 5: Be SELECTive"}

In general, it's best practice to only select the columns that you need. For example, if you wanted to see the names and hire dates of the various employees, you could show that with the following query:

```SQL
SELECT * FROM employees;
```

![Sample Select All from Employees Table](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/e-sample_select_all_query.png)

Notice how the query loads 300,024 rows in about 0.26 seconds. With the `EXPLAIN` statement, we can see that the entire table is being scanned, which makes sense because we are looking at all the entries.

If we, however, only wanted to see the names and hire dates, then we should select those columns:

```SQL
SELECT first_name, last_name, hire_date FROM employees;
```

![Sample First Name, Last Name and Hire Date from Employees Table](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/e-select_specific_columns_query.png)

As you can see, this query was executed a little faster despite scanning the entire table as well.

Give this a try!

## Practice Exercise 1

Let's take a look at the **salaries** table. What if we wanted to see how much each employee earns?

When running the query, keep in mind how long it takes the query to run and how many rows are scanned each time.

1. First, let's select all the rows and columns from this table.
    <details>
    <summary>Hint (Click Here)</summary>

    You'll need two separate queries: one to view the query and output, and another to see how many rows are run through.
    </details>

    <details>
    <summary>Solution (Click Here)</summary>
    To select all the rows and columns, we'll use the following query:

    ``` SQL
    SELECT * FROM salaries;
    ```
    
    
    Although the exact time may differ, in this instance, it took about 1.71 seconds to load 2,844,047 rows.

    We can check how many rows were scanned with the following statement:

    ``` SQL
    EXPLAIN SELECT * FROM salaries;
    ```
    

    We can see that almost the entire table was scanned, as expected, totalling to 2,838,426 rows.

    ![Practice Exercise 1 Part 1 Output](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/e-practice_exercise1_output.png)

    </details>

2. Now, let's see if there's a way to optimize this query. Since we only want to see how much each employee earns, then we can just select a few columns instead of all of them. Which ones would you select?

    <details>
    <summary>Hint (Click Here)</summary>

    You'll need two separate queries: one to view the query and output, and another to see how many rows are run through. Consider the columns in this table: **emp_no**, **salary**, **from_date**, and **to_date**.
    </details>

    <details>
    <summary>Solution (Click Here)</summary>

    To select columns that will give us information about the employee and their corresponding salary, we'll choose the **emp_no** and **salary** columns with the following query:

    ``` SQL
    SELECT emp_no, salary FROM salaries;
    ```
    

    Although the exact time may differ, in this instance, it took about 1.19 seconds to load 2,844,047 rows.

    We can check how many rows were scanned with the following statement:

    ``` SQL
    EXPLAIN  SELECT emp_no, salary FROM salaries;
    ```
    

    We can see that almost the entire table was scanned, as expected, totalling to 2,838,426 rows. Yet, it loaded faster than the first instance because we were more selective in the columns that were chosen.

    ![Practice Exercise 1 Part 2 Output](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/e-practice_exercise1-2_output.png)

    </details>

## Practice Exercise 2

Let's take a look at the **titles** table. What if we wanted to see the employee and their corresponding title?

Practice by selecting only the necessary columns and run the query!

<details>
<summary>Hint (Click Here)</summary>

You'll need two separate queries: one to view the query and output, and another to see how many rows are run through. Consider the columns in this table: **emp_no**, **title**, **from_date**, and **to_date**.

</details>

<details>
<summary>Solution (Click Here)</summary>

To select columns that will give us information about the employee and their corresponding title, we'll choose the **emp_no** and **title** columns with the following query:

``` SQL
SELECT emp_no, title FROM titles;
```

Although the exact time may differ, in this instance, it took about 0.22 seconds to load 443,308 rows.

We can check how many rows were scanned with the following statement:

``` SQL
EXPLAIN  SELECT emp_no, title FROM titles;
```

We can see that almost the entire table was scanned, as expected, totalling to 442,545 rows.

![Practice Exercise 2 Output](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/e-practice_exercise2_output.png)

In comparison, if you had run this with all columns selected, you may have noticed that it took about 0.47 seconds to load and scan the same amount of rows:

![Practice Exercise 2 Output](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/labs/MySQL/Lab%20-%20Improving%20Performance%20of%20Slow%20Queries%20in%20MySQL/images/e-practice_exercise2_output_selectall.png)

</details>

::page{title="Conclusion"}

Congratulations! Now, not only can you now identify common causes to slow queries, but you can resolve them by applying the knowledge that you have gained in this lab. Equipped with this problem-solving skill, you will be able to improve your queries performance, even in large databases.

## Author(s)

Kathy An

## Other Contributor(s)

Rav Ahuja

<!--

## Changelog

| Date | Version | Changed by | Change Description |
|------|--------|--------|---------|
| 2021-10-05 | 1.0 | Kathy An | Created initial version |
| 2022-09-06 | 1.1 | Lakshmi Holla | Made changes in practice exercise |
| 2023-05-08 | 1.2 | Eric Hao | Updated Page Frames |
-->

## <h3 align="center"> © IBM Corporation 2023. All rights reserved. <h3/>


::page{title="Hands-on Lab: Getting Started with Apache Airflow"}

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/images/SN_web_lightmode.png" width="300" alt="cognitiveclass.ai logo"><br/>


Estimated time needed: **20** minutes


## Introduction
In this lab, you will have the opportunity to work with Apache Airflow. You will work with both the Web user interface (UI) and command line interface (CLI) to explore the various ways you can use Airflow for workflow management.

## Objectives

After completing this lab, you will be able to:

-   Start Apache Airflow
-   Open the Airflow UI in a browser
-   List all the DAGs
-   List the tasks in a DAG
-   Explore a DAG in the UI

::page{title="About Skills Network Cloud IDE"}

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands on labs for course and project related labs. Theia is an open source IDE (Integrated Development Environment), that can be run on desktop or on the cloud. To complete this lab, we will be using the Cloud IDE based on Theia running in a Docker container.

## Important notice about this lab environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

::page{title="Exercise 1: Start Apache Airflow"}

1. Click on **Skills Network Toolbox**.
2. From the **BIG DATA** section, click **Apache Airflow**.
3. Click **Create** to start the Apache Airflow.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/9kHo-yaw-BZiErJ8cf9VNg/create.png" style="margin:.5cm;width:90%"/>

> **Note**: Please be patient, it will take a few minutes for Airflow to start.


::page{title="Exercise 2: Open the Airflow Web UI"}

1. When Airflow starts successfully, you should see an output similar to the one below.  Once **Apache Airflow** has started, click on the highlighted icon to open **Apache Airflow Web UI** in the new window.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/oOEvvbiaEKB_S_izc8BZLg/airflow-active.jpg" style="margin:1cm;width:90%"/>


2. You will land on a page that displays various DAGs and associated options.

<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/REjhlZPZksRQQK9mwX8AyA/airflowhomepage.jpg' style="width:90%;margin:1cm;"/>


3. You can unpause and pause a DAG using the **Unpause/Pause** toggle button.

> The button is grey when the DAG has been paused.

<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Getting%20Started%20with%20Apache%20Airflow/images/airflow_pause_unpause.png' style="width:50%;margin:.5cm;"/>

> The button is not greyed out when the DAG is running.

<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Getting%20Started%20with%20Apache%20Airflow/images/airflow_unpaused_dag.png' style="width:50%;margin:.5cm;"/>


4. Click on a DAG to explore more.

<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/tmplA1cgyfcLgU8ek8D2yw/clickdag.jpg' style="width:50%;margin:.5cm;"/>


5. You will see the `Grid` view by default.


<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/t3i1MGryOSX5qFC4AGs0sw/gridview.jpg' style="width:90%;margin:.5cm;"/>


6. Next, click on the **Graph** button.

<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/mF5Xu4SrcCCTHBmdkePHGg/graph-1.png' style="width:90%;margin:.5cm;"/>


7. Notice the graph view of the DAG will display.

<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/NHrA1t-080VKVlgjYTJw3A/graphview.jpg' style="width:90%;margin:.5cm;"/>


::page{title="Exercise 3: Apache Airflow CLI"}

Apache Airflow provides some command line options.

1. Run the command below in the terminal to list all the existing DAGs.

	```bash
	airflow dags list
	```

2. Run the command below in the terminal to list all tasks in the DAG named `example_bash_operator`.

	```bash
	airflow tasks list example_bash_operator
	```

### Practice Exercise
1. Run a command to list all tasks for the DAG named `tutorial`.
<details>
	<summary><font color="#007D79">Click here for the <b>solution</b>.</font></summary>

	```bash
	airflow tasks list tutorial
	```
</details>


::page{title="Exercise 4: Pause or Unpause a DAG"}

1. Run the command below in the terminal to unpause a DAG named `tutorial`.

	```
	airflow dags unpause tutorial
	```

2. Run the command to pause the DAG.

	```
	airflow dags pause tutorial
	```

### Practice Exercise
1. Run a command to unpause the DAG named `example_branch_operator`.
<details>
	<summary><font color="#007D79">Click here for the <b>solution</b>.</font></summary>

	```
	airflow dags unpause example_branch_operator
	```
</details>


::page{title="Practice exercises"}

1. List tasks for the DAG `example_branch_labels`.

<details>
	<summary><font color="#D02670">Click here for <b>hint</b>.</font></summary>

> Use `list` option.

</details>

<details>
	<summary><font color="#007D79">Click here for the <b>solution</b>.</font></summary>


```
airflow tasks list example_branch_labels
```

</details>


2.  Unpause the DAG `example_branch_labels`.

<details>
	<summary><font color="#D02670">Click here for <b>hint</b>.</font></summary>

> Use the unpause option.

</details>

<details>
	<summary><font color="#007D79">Click here for the <b>solution</b>.</font></summary>

```
airflow dags unpause example_branch_labels

```

</details>

3. Pause the DAG `example_branch_labels`.

<details>
	<summary><font color="#D02670">Click here for <b>hint</b>.</font></summary>
	
> Use the pause option.

</details>

<details>
	<summary><font color="#007D79">Click here for the <b>solution</b>.</font></summary>

```
airflow dags pause example_branch_labels
```

</details>

## Authors

Ramesh Sannareddy
[Lavanya T S](https://www.linkedin.com/in/lavanya-sunderarajan-199a445/)

### Other Contributors
Rav Ahuja

<!-- ## Change Log

| Date (YYYY-MM-DD) | Version | Changed By        | Change Description                 |
| ----------------- | ------- | ----------------- | ---------------------------------- |
| 2024-06-05        | 2.0     | Lavanya |Initial revision|
| 2021-07-05        | 1.0     | Ramesh Sannareddy | Created initial version of the lab |

-->

<h3 align="center"> &#169; IBM Corporation. All rights reserved. <h3/>


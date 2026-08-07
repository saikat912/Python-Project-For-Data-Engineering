::page{title="Hands-on Lab: Monitoring a DAG"}


<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/module%201/images/SN_web_lightmode.png" width="300" alt="cognitiveclass.ai logo"><br/>


Estimated time needed: **20** minutes

## Introduction
In this lab, you will work with the Airflow Web UI and CLi to explore the DAGs further. You will be exposed to using the interactive tools to search for DAGs, introduces to various views of the DAGS and how you can use this to explore the DAG workflow, the individual tasks in the workflow and view the outcome of the tasks.

## Objectives

After completing this lab you will be able to:

-   Search for a DAG
-   Pause/Unpause a DAG
-   Get the Details of a DAG
-   Explore grid view of a DAG
-   Explore graph view of a DAG
-   Explore Calendar view of a DAG
-   Explore Task Duration view of a DAG
-   Explore Details view of a DAG
-   View the source code of a DAG
-   Delete a DAG

::page{title="About Skills Network Cloud IDE"}

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands on labs for course and project related labs. Theia is an open source IDE (Integrated Development Environment), that can be run on desktop or on the cloud. to complete this lab, we will be using the Cloud IDE based on Theia running in a Docker container.

## Important notice about this lab environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

::page{title="Exercise 1: Start Apache Airflow"}

1. Click on **Skills Network Toolbox**.
2. From the **BIG DATA** section, click **Apache Airflow**.
3. Click **Create** to start the Apache Airflow.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/9kHo-yaw-BZiErJ8cf9VNg/create.png"/>

> **Note**: Please be patient, it will take a few minutes for Airflow to get started.




::page{title="Exercise 2: Open the Airflow Web UI"}

When Airflow starts successfully, you should see an output similar to the one below.  Once **Apache Airflow** has started, click on the highlighted icon to open **Apache Airflow Web UI** in the new window.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/oOEvvbiaEKB_S_izc8BZLg/airflow-active.jpg" style="margin:.5cm;width:90%"/>


You should land at a page that looks like this.

<img src='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/REjhlZPZksRQQK9mwX8AyA/airflowhomepage.jpg' style="width:90%;margin:.5cm;"/>


::page{title="Exercise 3: Submit a dummy DAG"}

For the purpose of monitoring, let\'s create a dummy DAG with three tasks.

- Task1 does nothing but sleep for 1 second.

- Task2 sleeps for 2 seconds.

- Task3 sleeps for 3 seconds.

This DAG is scheduled to run every 1 minute.

1. Using Menu->`File`->`New File` create a new file named `dummy_dag.py`.

2. Copy and paste the code below into it and save the file.

```python
# import the libraries

from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Your name',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    'dummy_dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval=timedelta(minutes=1),
)

# define the tasks

# define the first task

task1 = BashOperator(
    task_id='task1',
    bash_command='sleep 1',
    dag=dag,
)

# define the second task
task2 = BashOperator(
    task_id='task2',
    bash_command='sleep 2',
    dag=dag,
)

# define the third task
task3 = BashOperator(
    task_id='task3',
    bash_command='sleep 3',
    dag=dag,
)

# task pipeline
task1 >> task2 >> task3

```

3. Set the `AIRFLOW_HOME` directory.

	```bash
	export AIRFLOW_HOME=/home/project/airflow
	```

4. Submitting a DAG is as simple as copying the DAG python file into `dags` folder in the `AIRFLOW_HOME` directory. Open a terminal and run the command below to submit the DAG.

	```
	cp dummy_dag.py $AIRFLOW_HOME/dags
	```

5. Verify that our DAG actually got submitted. Run the command below to list out all the existing DAGs.

	```
	airflow dags list
	```

6. Verify that `dummy_dag` is a part of the output.

	```
	airflow dags list | grep dummy_dag
	```

6. Run the command below to list out all the tasks in `dummy_dag`.

	```
	airflow tasks list dummy_dag
	```

>You should see 3 tasks in the output.

::page{title="Exercise 4: Search for a DAG"}

1. In the Web-UI, identify the `Search DAGs` text box as shown in the image below and type `dummy_dag` in the textbox and press enter.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/GRNUom2cQhIq4y2kBPo4Jw/search-dag.jpg" style="width:90%; margin:.5cm"/>

Note: It may take a couple of minutes for the dag to appear here. If you do not see your DAG, please give it a minute and try again.

2. You should see the `dummy_dag` listed as seen in the image below:


<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/n4cbg0ugiIWoY5cLrpUOkA/dummy-dag.jpg" style="width:90%; margin:.5cm"/>

::page{title="Exercise 5: Pause/Unpause a DAG"}

1. Unpause the DAG using the Pause/Unpause button.


<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/TTYgOeoyShNPEj0pJU0cNw/pause%20unpause.jpg" style="width:90%; margin:.5cm"/>


2. You can see the following details in this view.

- Owner of the DAG
- How many times this DAG has run
- Schedule of the DAG
- Last run time of the DAG
- Recent task status

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/oEznTFz4sciAq_oenJG2Xg/dag-unpaused.jpg" style="width:90%; margin:.5cm"/>


::page{title="Exercise 6: Detailed view of a DAG"}

1. Click on the DAG name as shown in the image below to see the detailed view of the DAG.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/95rZrkWU75XI7pWUag3dFA/clickdagname.jpg" style="width:90%; margin:.5cm"/>


2. You will land on a DAG details page showing the default grid view with the three tasks listed.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/W1nyIK0KyWH6tH98n8o4TQ/dag%20details.jpg" style="width:90%; margin:.5cm"/>

The Grid view shows your DAG tasks in the form of grids as seen in the image. You will observe the `Auto Refresh` button switched on by default on the right corner.

The grids in the image represent a single DAG run and the color indicates the status of the DAG run. Place your mouse on any grid to see the details.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/BFtZ7JwaxIc3JV7NKq8OZQ/dag-status.jpg
" style="width:90%; margin:.5cm"/>


The squares in the image below represent a single task within a DAG run and the color indicates its status. Place your mouse on any square to see the task details.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/9muJx8FAZu6U2hNQSEUcJw/task-status.jpg" style="width:90%; margin:.5cm"/>


::page{title="Exercise 7: Explore graph view of DAG"}

1. Click on the `Graph View` button to open the graph view. The graph view shows the tasks in a form of a graph. With the auto refresh on, each task status is also indicated with the color code.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/U5Bo4l1orMEcHswT_xKRtQ/graph-view.jpg" style="width:90%; margin:.5cm"/>

::page{title="Exercise 8: Calender view"}

The calender view gives you an overview of all the dates when this DAG was run along with its status as a color code.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/UsVOBsRcf1XlGs31IuZ2dA/calendar-view.jpg" style="width:90%; margin:.5cm"/>


::page{title="Exercise 9: DAG and Task Duration view"}

The DAG duration gives you an overview of how much time the entire workflow took.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/CG5Z2evazF8GBiK-tTA1rQ/dag-duration.jpg" style="width:90%; margin:.5cm"/>


The Task Duration view gives you an overview of how much time each task took to execute, over a period of time.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/vL3tJ1Xn1lwDvjJ4IES04Q/task-duration.jpg" style="width:90%; margin:.5cm"/>


::page{title="Exercise 10: Details view"}

The Details view give you all the details of the DAG as specified in the code of the DAG.


<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/1HJa2BqXFsAPV7m_Ew1FgA/dag-details.jpg" style="width:90%; margin:.5cm"/>

::page{title="Exercise 11: Code view"}

The Code view lets you view the code of the DAG.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/K-ZXIgH0_Nn7VOr5jl89YA/dag-code.jpg" style="width:90%; margin:.5cm"/>

::page{title="Exercise 12: Task logs"}

You can view the logs of an individual task with task logs.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/C0yFNUn3vW1YDo7Zein5iw/task-logs.jpg" style="width:90%; margin:.5cm"/>



::page{title="Exercise 13: Delete a DAG"}

To delete a DAG click on the delete button.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/Zp2ywy1m3a0unffHmXSfaw/delete-dag.jpg" style="width:90%; margin:.5cm"/>



You will get a confirmation pop up as shown in the image below. Click `OK` to delete the DAG.

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/p2dpSmVYyNLHgvpyp5BaBg/confirm-deletion.jpg" style="width:50%; margin:auto;display:flex"/>

::page{title="Practice exercises"}

1. Unpause any existing DAG and monitor it.

2. View the details on any existing DAG. View the code of the DAG. Delve into the task details and view the logs of each task.

## Authors

[Lavanya T S](https://www.linkedin.com/in/lavanya-sunderarajan-199a445/)
Ramesh Sannareddy

### Other Contributors

Rav Ahuja

<!--
## Change Log

| Date (YYYY-MM-DD) | Version | Changed By        | Change Description                 |
| ----------------- | ------- | ----------------- | ---------------------------------- |
| 2024-06-06        | 2.1     | Mercedes Schneider | QA pass with edits |
| 2024-06-06        | 2.0     | Lavanya T S | Created version 2 |
| 2021-07-05        | 1.0     | Ramesh Sannareddy | Created initial version of the lab |

-->

<h3 align="center"> &#169; IBM Corporation. All rights reserved. <h3/>


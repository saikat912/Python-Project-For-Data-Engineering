::page{title="Hands-on Lab: Working with Streaming Data using Kafka"}

<img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/images/SN_web_lightmode.png" alt="cognitiveclass.ai logo" width="300" />  
  

Estimated time needed: **20** minutes

## Introduction

In this lab, you will work with streaming data using Kafka. You will start by configuring the Kafka server to use the Kraft mode followed by starting the Kafka message broker service, creating a topic and then starting the producer and consumer.

## Objectives

After completing this lab, you will be able to:

-   Download Kafka binaries
    
-   Configure the Kafka server to use the KRaft mode
    
-   Start the Kafka message broker service
    
-   Create a topic
    
-   Start a producer
    
-   Start a consumer
    

::page{title="About Skills Network Cloud IDE"}

Skills Network Cloud IDE (based on Theia and Docker) provides an environment for hands-on labs for course and project-related labs. Theia is an open-source IDE (Integrated Development Environment), that can be run on desktop or on the cloud. To complete this lab, we will be using the Cloud IDE based on Theia running in a Docker container.

## Important notice about this lab environment

Please be aware that sessions for this lab environment are not persistent. A new environment is created for you every time you connect to this lab. Any data you may have saved in an earlier session will get lost. To avoid losing your data, please plan to complete these labs in a single session.

::page{title="Exercise 1: Download and extract Kafka"}

1.  Open a new terminal by clicking the menu bar and selecting **Terminal**\->**New Terminal**, as shown in the image below.
    
    <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Streaming/images/new-terminal.png" alt="Terminal menu with New Terminal highlighted." width="75%" />
    
    This will open a new terminal at the bottom of the screen.
    
    <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Streaming/images/terminal_bottom_screen.png" alt="New terminal instance." width="75%" />
    

##### Next, run the following commands on the terminal.

2.  Download Kafka by running the command below:
    
    ```bash
    wget https://archive.apache.org/dist/kafka/3.8.0/kafka_2.13-3.8.0.tgz
    
    ```
    
3.  Extract Kafka from the zip file by running the command below.
    
    ```bash
    tar -xzf kafka_2.13-3.8.0.tgz
    
    ```
    

This command will create a new directory `kafka_2.13-3.8.0` in the current directory.

::page{title="Exercise 2: Configure KRaft and start server"}

1.  Navigate to the `kafka_2.13-3.8.0` directory.
    
    ```bash
    cd kafka_2.13-3.8.0
    
    ```
    
2.  Generate a cluster UUID that will uniquely identify the Kafka cluster.
    
    ```bash
    KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
    
    ```
    
    This cluster id will be used by the KRaft controller.
    
3.  KRaft requires the log directories to be configured. Run the following command to configure the log directories passing the cluster ID.
    
    ```bash
    bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
    
    ```
    
4.  Now that KRaft is configured, you can start the Kafka server by running the following command.
    
    ```
    bin/kafka-server-start.sh config/kraft/server.properties
    
    ```
    
    You can be sure that the Kafka server has started when the output displays messages like "Kafka Server started".
    

![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/aN0HsMMBWXxj8gPhA8BVyg/KafkaStarted.jpg)

::page{title="Exercise 3: Create a topic and start producer"}

You need to create a topic before you can start to post messages.

1.  Start a new terminal and change to the `kafka_2.13-3.8.0` directory.
    
    ```bash
    cd kafka_2.13-3.8.0
    
    ```
    
2.  To create a topic named `news`, run the command below.
    
    ```
    bin/kafka-topics.sh --create --topic news --bootstrap-server localhost:9092
    
    ```
    
    You will see the message: `Created topic news.`
    
3.  You need a producer to send messages to Kafka. Run the command below to start a producer.
    
    ```
    bin/kafka-console-producer.sh   --bootstrap-server localhost:9092   --topic news
    
    ```
    
4.  After the producer starts, and you get the '>' prompt, type any text message and press enter. Or you can copy the text below and paste. The below text sends three messages to Kafka.
    
    ```
    Good morning
    Good day
    Enjoy the Kafka lab
    
    ```
    

::page{title="Exercise 4: Start Consumer"}

You need a consumer to read messages from Kafka.

1.  Start a new terminal and change to the `kafka_2.13-3.8.0` directory.
    
    ```bash
    cd kafka_2.13-3.8.0
    
    ```
    
2.  Run the command below to listen to the messages in the topic `news`.
    
    ```
    bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic news   --from-beginning
    
    ```
    
3.  You should see all the messages you sent from the producer appear here.
    
4.  You can go back to the producer terminal and type some more messages, one message per line, and you will see them appear here.
    

::page{title="Exercise 5: Explore Kafka directories"}

Kafka uses the **/tmp//tmp/kraft-combined-logs** directory to store the messages.

1.  Start a new terminal and navigate to the `kafka_2.13-3.8.0` directory.
    
    ```bash
    cd kafka_2.13-3.8.0
    
    ```
    
2.  Explore the root directory of the server.
    
    ```
    ls
    
    ```
    
3.  Notice there is a `tmp` directory. The `kraft-combine-logs` inside the `tmp` directory contains all the logs. To check the logs generated for the topic `news` run the following command:
    
    ```
    ls /tmp/kraft-combined-logs/news-0
    
    ```
    

> **Note**: All messages are stored in the `news-0` directory under the **/tmp/kraft-combined-logs** directory.

::page{title="Exercise 6: Clean up"}

##### To stop the producer

In the terminal where you are running producer, press `CTRL+C`.

##### To stop the consumer

In the terminal where you are running consumer, press `CTRL+C`.

##### To stop the Kafka server

In the terminal where you are running Kafka server, press `CTRL+C`.

::page{title="Practice exercises"}

1.  Create a new topic named `weather`.
    

<details>
<summary>Click here for a hint.</summary>
<blockquote><p>Use <code>kafka-topics.sh</code> command with the <code>create</code> option.</p></blockquote>
</details>

<details>
<summary>Click here for the solution.</summary>
<p>Make sure that the Kafka server is still running. Change to the <code>kafka_2.13-3.8.0</code> directory and run the following command:</p><pre><code>bin/kafka-topics.sh --create --topic weather --bootstrap-server localhost:9092
</code></pre>
</details>

2.  Post messages to the topic `weather`.
    

<details>
<summary>Click here for a hint.</summary>
<blockquote><p>Use <code>kafka-console-producer.sh</code> and point to topic <code>weather</code>.</p></blockquote>
</details>

<details>
<summary>Click here for the solution.</summary>
<p>Make sure that the Kafka server is still running. Run the following command:</p><pre><code>bin/kafka-console-producer.sh   --bootstrap-server localhost:9092   --topic weather
</code></pre><p>Post some test messages.</p>
</details>

3.  Read the messages from the topic `weather`.
    

<details>
<summary>Click here for a hint.</summary>
<blockquote><p>Use <code>kafka-console-consumer.sh</code> and read from the topic 'weather'.</p></blockquote>
</details>

<details>
<summary>Click here for the solution.</summary>
<p>Make sure that the Kafka server is still running. In a new terminal, change to <code>kafka_2.13-3.8.0</code> directory and run the following command:</p><pre><code>bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic weather
</code></pre><p>Make sure that the messages you sent from the producer appear here.</p>
</details>

## Authors

[Lavanya T S](https://www.linkedin.com/in/lavanya-sunderarajan-199a445/)

### Other Contributors

Rav Ahuja

### © IBM Corporation. All rights reserved.

&nbsp;

# Monitor machine load application

Simple web application that monitors load average on your machine

Assignment requirements:

Create a simple web application that monitors load average on your machine:

Collect the machine load (using the “uptime” command for example)

The web application should serve a single page: a list of key statistics as well as a history of load over the past 10 minutes in 10s intervals. (Don’t worry about getting fancy here, just a simple list is fine). Don’t worry about persisting historical data beyond the life the process.

Whenever the load for the past 2 minutes exceeds 1 on average, add a message to the history saying that “High load generated an alert - load = {value}, triggered at {time}”

Whenever the load average drops again below 1 on average for the past 2 minutes, Add another message explaining when the alert recovered.

Write unit tests for the alerting logic

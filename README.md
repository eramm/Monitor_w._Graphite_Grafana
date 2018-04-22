# Monitor_w._Graphite_Grafana
Background from Ori

You have a cat. The cat eats only fish, milk and bread.
You are to use set of tools that alert you if the cat was hungary more than a certain amount of time.

The tools set should include monitoring tool (e.g. Nagios), time series DB (e.g. statsd), and a time series
visualisation tool (e.g. graphite/grafana).
The tools should be deployed on the cloud in an automatically as possible manner (e.g. with Docker and Kubernetes).
You should create free account for Google Cloud or AWS in case you don’t already have (It’s free of charge so no
worries).

Feeding the "cat" should be done by a simple script (e.g. in Python with statsd library) that send metrics called
"fish", "bread" or "milk" to the time series DB.

If more than 15 minutes passed and the cat has not eaten at least two pieces of food (e.g. milk and another milk, or
milk and bread), you receive an alert that kindly reminds you to feed him. After all, he *is* your cat.
If the cat hunger condition go back to normal, you get an email alert that the cat is "back to normal".
Notification destinations currently include email (or Slack), and a viewable audit log (e.g. the UI of Nagios).

In addition, you should use a visualization dashboard which through it you can see the metrics in a graph in adjustable
time frame.


Background from Eliezer:

This was a big ask and I was only able to commit to producing the first half in the short time frame given and my other commitments at this time.


So here is what I did:

Stage 1 - Launch a server to run Carbon-Cache/Graphite and Grafana

Associated files

srcs/carbon/etc/carbon/storage-schemas.conf
srcs/carbon/etc/carbon/storage-aggregation.conf


Important changes - since we are sending a small amount of data every x minutes as opposed to a steam of data which is more of what Graphite is built for we set the retention schema to 

1m:1d,5m:2y and a xFilesFactor = 0 So the non streaming data would be retained. In our cased we say that one days worth of data would contain datapoints from within a 1 minute window. We set the the "xFilesFactor" to 0 since we only send one data packet to the whisper database and there is no need to sample or have carbon work with a ratio of packets.

srcs/python/feedkitty.py

this is a simple python script that does 2 things

1) It chooses from a random element of a Python dictionary (key/value DB) where we assign each food a weight of 25 or 0 for no food
2) It takes the value from above and and posts it to Carbon using Netcat.

** note Carbon and StatsD do essentially the same thing but StatsD is able to handle loads much better Hence I did not use StatsD

We installed the script in Cron and have it run every  7 minutes

We can then see it in Graphite.

Adding Grafana to the Picture -

Setting up Grafana is pretty straight forward. Configure your Graphite instance as a datasource, create a new Dashboard and load it with your metric. In our Case changing the default line graph to a bar graph gave a better and more consistent picture. (Grafana was acticting quirky in line graph mode by not allowing to drill down to less than a few hours)

So Now in Grafana we can see a bar that equals 25 or a gap where no food was given.

Nagios 

I set this up on a seperate box to save myself the trouble of configuring Apache with another website on a odd port.

Classic setup wih NRPE for remote  execution of code on the Graphite/Grafana box.

Back on the Graphite box (Graphite-1) I wrote a check - CHECK_KITTY in python that does 2 things

1) It polls 15 minutes of data from the whisper DB (i.e. graphite back-end) and then adds the results to see if we have the equivalent of 2 snacks (50) . If yes it sends an OK to Nagios. If less than sends a warning to Nagios and if zero send a critical message

The results from CHECK_KITTY show up in the Nagios interface (can be seen from the services page)

When a Critical alert (must fail 4 times could be changed) is issued then it's sent to PagerDuty for alerting.



note the 'r' option in the Nagios keyword 'notification_options' instructs nagios to send an email on recovery.


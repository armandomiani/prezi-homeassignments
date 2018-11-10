# Prezi Exam - Armando Miani

## Application Architecture

### Back-end

The application's backend would be built on top of RESTful microservices, providing a collection of loosely coupled services..

Each service would have different resources for solving a domain-specific problem. E.g.::

* **Accounts API** - responsible for managing authentication, authorization and access control to multiple products;
* **Billing API** - responsible for managing customers' billing, invoices, charging, discounts, coupons and chargebacks;
* **Management API** - responsible for managing all application settings;
* **Logging API** - responsible for handling logs of each part of the application;
* **Reporting API** - responsible for providing statistical data taking advantage of technologies such as BigData/BI.

### Front-end

Multiple clients would be created according to reviews on  the public who will be using  the application. For example, Uber does not have a different applications for Executives and Cooks, but it does for the Drivers and Passengers.

No domain logic would be present on client-side. All data access would be made across the APIs, where domain logic will be


## Development

### Programming Languages

Modern, dynamic, large and active community, lots of libraries, a decent dependency manager and good maintainability would be parameters for picking a programming language.

Python meets all those requirements and would be chosen as the main back-end language.

Certainly it is not possible to avoid the need to use another language in the project. If the application has a requirement where another language would fit better, it is always possible to create a microservice using another language in order to solve a specific  issue. R and Ruby would be strong candidates when writing a Reporting API and a Logstash Plugin, for example.

Looking into the API, Bottle, Flask and Falcon frameworks are all good options, but Bottle would be the winner. Although Flask has more available extensions, it is not as faster as Bottle and the Falcon resources are class-based, which becomes harder to maintain. Bottle is lighter, simpler and easier to debug and maintain.

Each web client would be created using a Single-Page Application (SPA) approach and a popular framework, such as React.

Mobile clients would be well analyzed about the real need of creating a native application or a web approach.

### Branching

The branching strategy should be a mix of Task Branching and Release Branching. Every task (Features and Bugs) should have a branch. Two branches should be connected to a Continuous Integration, as follows: master (Production) and staging. When new features are completed, they would be merged to a Release branch - all the new features should be merged to staging via pull request, approved and promoted to master. All master releases would be tagged with its version.

## Deployment

Gitlab would be chosen as the source-code repository of the project. Gitlab has a better issue tracker and a continuous integrationto the source-code and issues.

At least two pipelines would be set on Gitlab CI: Production and Staging. Both pipelines would run local unit tests and RunScope API tests.

During the deployment process it is important to increase the desired number of instances, deploy the new release and be sure that the new instance are up and responding well to the health checks before removing the older ones from the Load Balancer, providing a zero downtime deploy.

## Scaling-out

Amazon Elastic Container Service would be the base for each component of the application - a Docker Container is easier to deploy and the developers are able to work with an environment identical to the production's.

The application's domain would point to a HA Proxy cluster which would have  an Elastic Container Service as its target. We could have used ELB here, but it is slow to accept quick changes during the day and we want to have the flexibility to change the haconfig file which directly points to the application's webservers (nginx).

The HA Proxy would point to a Varnish cluster in order to add caching capabilities to our application. Caching strategy is a sneaky issue, and we would have to take care about some parameters (such as user-agent and ip in some cases), and have a good data invalidation strategy.

The Python application should run over uWSGI, taking advantage of the number of cores on the containers' hosts.

About the database access, we would need to have a good redundancy strategy. If we are in a read-intensive scenario, we would use a distributed MongoDB with RAID hard-disks.

For BI scenarios, I would use cloud-based tools such as: Redshift or Google BigQuery (which performs really good for big amount of data and you do not have to care about backups and reliability).

In this particular case, Redshift would be used because we are already in an Amazon environment and Redshift is quite more "SQLly" than BigQuery.

## Monitoring

Runscope would help to periodically test the API out of the application's environment.

AWS SNS would help to notify events from Amazon services -AWS CloudTrail would move SNS log entries to a bucket in S3.

Logstash would centralize different log files from Webservers, Databases and S3 to a Elasticsearch server.

Kibana would provide different dashboards against our Elasticsearch in order to keep the team always aware.

The main metrics we would follow must be targeted to the customers' experience, such as:

- Response Time
- Requests/Sec
- Number of Users Connected
- Prediction of Requests/Sec in next hours
- Users' turnover (Users sign-in and out) in the last x minutes vs Prediction of Users' turnover
- Number of instances running

## Logging

Greylog is better than Kibana for Devops team because we are able to deliver more details and setting specific permissions to each member.

Statistics has no limits,  so we can measure anything from the production code to the development team performance. We can measure how much the number of deploys impacts the application's performance. But at the end of the day, the customer experience is the most important thing to really care about.

This is, for sure, a top of mind architecture for a general application, which is quite different than something I would make knowing the real requirements of a real-world application, but I think it is an initial approach that can be a starting point for any kind of software service. :)

Best regards,

Armando Miani


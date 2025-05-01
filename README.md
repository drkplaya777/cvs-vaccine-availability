# Overview
I created an application to help my family and friends book appointments at CVS when
the rona ran wild in these streets. The government announced the jab and CVS secured
supply. They allowed people to book appointments, but the spots were booked before anyone could 
secure a spot. I built this application to solve that problem. 

The application polls CVS APIs for COVID immunization appointments in a set of cities. If a CVS 
in the city has availability the application generates an email and sends it to an email address. 
Run add new watcher adds a new recipient by command line while run celery worker starts polling CVS.

As a result this application booked appointments in Puerto Rico, California, New York and Georgia.
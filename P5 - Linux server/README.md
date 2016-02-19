# Project 5 - Linux server configuration
1- The IP address and SSH port so your server can be accessed by the reviewer.
in order to access the server use this command ==>
``` bash 
ssh -i udacity.rsa grader@52.32.135.74 -p 2200
```
The key udacity.rsa is provided in the student notes 

2- The complete URL to your hosted web application.
`http://52.32.135.74`

3- A summary of software you installed and configuration changes made
* anacron - the cron job that takes the cronjob defined in /etc/cron.* folder
* apache2 - the web server. configured it to work on /var/www/catalog as main folder
* postgress - configured that no remote connection availble. add user catalog with superuser privileges
* git - to download the code from the repo
* ufw - Basic firewall, configured to enable only port 443, 80 and 2200 to login to the server. also configured it to limit ssh access to 6 tries. (`ufw limit ssh/tcp`)

4- A list of any third-party resources you made use of to complete this project
* munin -  software that can monitor the server status, and creates alert for the server


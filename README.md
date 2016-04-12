# bypass-portal-remotely
A tool to temporarily disable the webportal in case of issues. 

I made this script because we had too many instances of agents hashing out the wrong lines in the conf file and breaking the system.
Secondary concern was that when agents unhashed the lines after resolving the Incident, they often made some small mistake and altered the MD5sum of the file from the fleet standard. This made version control very difficult.

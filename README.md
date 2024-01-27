# Parse Free Logs

To generate the log file use the following command:
`free -m -s 1 | ts '%s' > free-output.log` 

`python parse_linux_free.py free-output.log`

`python parse_linux_free.py free-output.log --plot`

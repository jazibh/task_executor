Task Executor Python
====================


## Purpose
This repository use Python flask docker based application to read yaml format files and execute the commands specified. It also stores the output, if storage flag is set.

### Components
* Python flask application containerised with Docker.
* `main.py` contains the implementation of core logic.
* `input.yaml` file contains yaml formatted executor commands.
* `Dockerfile` contains the steps use to assemble docker image.
### Execution Steps
##### Build Docker Image 
`docker image build -t executor_docker . `
After building the image, run a container using this image.
##### Run the container
`docker run -p 5000:5000 -d executor_docker`
This runs the container on port `5000` using a port-binding approach.
We can access application by send a request to `localhost:5000` on our browser.


### Output
* Based on the supplied input in `input.yaml`, application will parse and execute those commands.
* Output is stored in a file `task-executor-output.txt` which is accessed via ssh into docker container.
`docker exec -it <container name> /bin/bash`

### Execution Logic
* `main.py` receives HTTP request. It reads from `input.yaml` file and execute instructions as shell commands.
* It stores the command name and its output as key/vaulue pair. If command is referenced in the subsequent commands its output will be reused."
* It also checks for any placeholder mentioned in the command and replace the placeholder with an output from earlier commands.
* Checks for `storage_output` flag and store the output in the file if flag is set

### Parallel Executions
* [Without considering placeholders] Parallel executions can be done in python using `multiprocessing` library. When we read command, we will assign its execition to a separate thread. In this way reading of command and executions of commands will run in parallel.
* [Considering placeholders] In case of placeholder (Reference of one command output in another command) we will have to use dependency graph. We will do multiprocessing and runs command in parallel but if we encounter any command which has placeholder/ dependency on some other command this command will wait until its dependent command is not compeleted.
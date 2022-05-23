from flask import Flask, render_template
import os
import yaml
import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


app = Flask(__name__)


@app.route('/')
def home():

    path = os.getcwd()

    logger.info("Creating a python dict 'results', that will store the command name and its output as key/vaulue pair.")
    logger.info("If command is referenced in the subsequent commands its output will be reused.")
    results = {}

    with open(path+"/input.yaml", "r") as stream:
        try:
            file = yaml.safe_load(stream)

            list = file['taskExecutorCommands']
            for item in list:

                command = item['command']
                
                match_result = re.search("{{.+}}", command)

                if match_result:
                    
                    logger.info("Found subcommand place holder")

                    logger.info("Spliting results to trim and get the name of command which is referenced in the current command")
                    list_commands = re.split('\s+', str(match_result.group()))

                    logger.info("Returning the output of the command which is referenced inside placeholder")
                    sub_command = results[(list_commands[1].split(".")[0]).split("command",1)[1]]
                    
                    logger.info("Replacing the placeholder with the results of command")
                    updated_command = command.replace(str(match_result.group()),sub_command)

                    logger.info("Executing as a bash command")
                    shell_exe=os.popen(updated_command)
                    
                else:
                    
                    logger.info("No matching sub command place holder")

                    logger.info("Executing as a bash command")
                    shell_exe=os.popen(item['command'])
                
                logger.info("Reading shell output results")
                shell_output=shell_exe.read()
                
                logger.info("Storing name and results the command executed")
                results[item['name']] = str(shell_output)
                
                logger.info("Output: command execution result " + str(shell_output))
                
                key = 'store_output'

                if key in item: 

                    if item['store_output'] == True:

                        try:
                            logger.info("Writing the output of task executor in a file")
                            with open("task-executor-output.txt", "a") as outfile:
                                outfile.write(str(shell_output))                          
                        
                        except Exception as exc:
                            logger.error("Error occurred while writing ouput")
                            logger.error(exc) 
                    
                    else:
                        logger.info("store_output is set as false. Command output will not be written in file")      
                
                else:
                    logger.info("store_output not found. Command output will not be written in file")

        except yaml.YAMLError as exc:
            logger.error("Error occurred while reading input file")
            logger.error(exc)

    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

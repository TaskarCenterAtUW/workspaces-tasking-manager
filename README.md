# Tasking Manager

### Dev Setup
1. Download the proper .env file from the TCAT Lab Google Drive: https://drive.google.com/drive/folders/1CDr-Xn1GuCatGq5i5txj_htmJLGHzVoG. Put the file in the root of this project, e.g. as ```dev.env```.

2. Add the following to your VS Code ```launch.json``` file and/or configure your IDE appropriately to connect to the debugger on port 5678 on demand:

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Attach",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678,
            },
            "pathMappings": [{
                "localRoot": "${workspaceFolder}/backend",
                "remoteRoot": "/usr/src/app/backend"
            }],
        },
    ]
}
```

3. Run: ```docker compose -f docker-compose.yml -f docker-compose.opensidewalks.yml --env-file dev.env --env-file tasking-manager.env build tm-frontend tm-backend-dev```. This layers the ```docker-compose.opensidewalks.yml``` file on top of ```docker-compose.yml```, and takes the ```tasking-manager.env``` file and replaces variables inside it with values from ```dev.env``` (NB: do *not* check this file into git). 

You have now built docker images for the TM. 

4. Run: ```docker compose -f docker-compose.yml -f docker-compose.opensidewalks.yml --env-file dev.env --env-file tasking-manager.env --profile dev up tm-backend-dev``` to start the backend TM docker image. 

The server will be listening on localhost:5001, and the pydebug debugger will be listening on port 5678. NB: the Python debug process will block until a debugger attaches to it.

5. If using VS Code, run step #4 above in the terminal inside VS Code. *The Python process will block until the debugger attaches*, so run the debugger from within VS Code, which should cause the terminal to emit messages related to it starting. 

6. You should now be able to set breakpoints within VS Code and access the TM at its URLs, e.g. ```http://localhost:5001/api/v2/workspaces/mine/?gig_only=true```

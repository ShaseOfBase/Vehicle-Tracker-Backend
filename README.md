# mms_gps_back

To run
1. Create a new virtual environment
2. pip install from requirements: pip install -r requirements.txt
3. Create a new mysql DB and add the relevant connection details in /db_env.py
4. Run 'pytest test_data.py' to confirm app is set up correctly and the DB can be reached. The tables will be created at this step or the next if this is skipped
6. From the root folder run 'python ./run.py' (running 'flask run' will run the wrong webserver on a port the front end doesn't know)
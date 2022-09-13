# mms_gps_back

To run
1. Create a new virtual environment (Python 3.8+ should be fine)
2. pip install from requirements: pip install -r requirements.txt
3. Create a new mysql DB and add the relevant connection details in /db_env.py
4. Run 'pytest test_data.py' to confirm app is set up correctly and the DB can be reached. The tables will be created at this step or the next if this is skipped
5. (Optionally) You may add some quick (and boring) dev data by running python ./_add_dev_data.py. The routes will be created completely at random, (likely some of them will be based in the sea, thus invalid and won't be displayed on the frontend.) The user for this data entry will be 'dev' and password 'abc123'
6. From the root folder run 'python ./run.py' (running 'flask run' will run the wrong webserver on a port the front end doesn't know)
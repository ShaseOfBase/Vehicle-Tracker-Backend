# mms_gps_back

To run
1. Create a new virtual environment
2. Switch to the virtual env and update pip: curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
3. switch to the root directory of this project and pip install from requirements: pip install -r requirements.txt
4. Create a new mysql DB and add the relevant connection details in /db_env.py
5. Run 'pytest test_data.py' to confirm app is set up correctly
6. run 'flask run'
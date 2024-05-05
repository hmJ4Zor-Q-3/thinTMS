:: maybe rebreak tests up by type into separate folders, unit, integration, etc. Then we can run them in terms of increasing complexity and decreasing speed. Perhaps cancelling all following sets if the prior had any issues.
python -m pytest src/test/
python -m robot --pythonpath . src/test/
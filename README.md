# Project Background
## Goal: 
For Mist MSP providers to easily track licences that are going to expire in next 30/60/90 days (Don't care about trial/eval licenses)
## Language: 
Python

# How to use

## Info Needed: 
Admin API token, Mist MSP ID

## Files:
- credential.py
Where admin API token and Mist MSP ID needs to be put in
- getLicense.py
Run API calls, get responses processed and results printed out
- requirement.txt
pip modules that needs to be installed for smooth run

Run getlicense.py for final results

# Results
## Output
Orgs with non-eval/commercial license(s) will be printed out
If license(s) going to expire in next 30/60/90 days, the license type and quantity will be printed out in proper table field under each orgs
### Example
|school-SG |30 day|60 day|90 day|       
|----------|------|------|------|


|Live Demo |30 day|60 day|90 day|
|:---------|------|------|:-----|       
|SUB-PMA | | |40|                                      
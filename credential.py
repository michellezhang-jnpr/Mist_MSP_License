#######
#
# credential.py
#
# Contains the Mist API configuration variables used for the 'getLicense.py'


# =========
# VARIABLES
# =========

# This is the Mist API tocken that mustbe included with each Mist API call.
mist_api_token = "your mist api token"
mist_api_path = "https://api.mist.com"

# This is the Mist 'MSP Site ID' for the excercise.
msp_id = ""  # The Mist Demo MSP

# This is the HTTP headers used for each Mist API call
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token " + mist_api_token,
}

import requests
import json
import sys
import pprint
from credential import *
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# =====
# FUNCTIONS
# =====


# Check Orgs under current MSP
def get_orgs(session, msp_id):
    url = mist_api_path + "/api/v1/msps/{}/orgs".format(msp_id)

    result = session.get(url, headers=headers)
    # pp.pprint(result)  # <Response [200]>

    if result.status_code != 200:
        print("Failed to GET")
        print("URL: {}".format(url))
        print("Response: {} ({})".format(result.text, result.status_code))
        return []

    result = json.loads(result.text)
    return result


# Check Licenses under each Org
def get_org_licenses(session, org_id):
    url = mist_api_path + "/api/v1/orgs/{}/licenses".format(org_id)

    result = session.get(url, headers=headers)

    if result.status_code != 200:
        print("Failed to GET")
        print("URL: {}".format(url))
        print("Response: {} ({})".format(result.text, result.status_code))
        return []

    result = json.loads(result.text)
    return result


def license_cell_builder(license):
    cell = {}
    cell["type"] = license["type"]
    cell["start_time"] = license["start_time"]
    cell["end_time"] = license["end_time"]
    cell["quantity"] = license["quantity"]

    return cell


# =====
# MAIN
# =====


# Ensure variables are defined
if mist_api_token == "" or msp_id == "":
    print("Missing variables:")
    print("mist_api_token={}".format(mist_api_token))
    print("msp_id={}".format(msp_id))

    sys.exit(1)

pp = pprint.PrettyPrinter(indent=4)
org_name_id_record = {}  # build blank dictionary record
master_list = {}  # org name with every licenses it has
tmp_org_licenses = []  # track licenses from each org
current_time = datetime.now()
# expiration_30_day_benchmark = date.today() + relativedelta(days=30)


# Create session
session = requests.Session()
result = get_orgs(session, msp_id)  # <class 'list'>

# get org name "name" and org id "id" out of the MSP Get response
for org in result:
    org_name_id_record[org["name"]] = org["id"]

# collect license details for each org
for org_name, org_id in org_name_id_record.items():
    org_licenses = get_org_licenses(session, org_id)
    # if the org has licenses
    if org_licenses["licenses"]:
        for license in org_licenses["licenses"]:
            if "SUB-Eval" not in license["subscription_id"]:
                tmp_org_licenses.append(license_cell_builder(license))
    # if amendment section exisit, might have some extra license info
    if "amendments" in org_licenses:
        for license in org_licenses["amendments"]:
            if "SUB-Eval" not in license["subscription_id"]:
                tmp_org_licenses.append(license_cell_builder(license))
    # if org has non-eval license
    if tmp_org_licenses:
        master_list[org_name] = tmp_org_licenses
        tmp_org_licenses = []

# pp.pprint(master_list)      # <class 'dict'>

# go through Master List and check licenses about to expire
for org_name, licenses in master_list.items():
    print("***** " * 11)
    print("\n")
    print("{:<25} {:<15} {:<15} {:<15}".format(org_name, "30 day", "60 day", "90 day"))
    for license in licenses:
        end_time = datetime.fromtimestamp(license["end_time"])
        # focus on non-expired licenses
        if end_time.date() >= current_time.date():
            days = (end_time - current_time).days
            # 30/60/90 day print out
            if days <= 30:
                print(
                    "{:<25} {:<15} {:<15} {:<16}".format(
                        license["type"], license["quantity"], "", ""
                    )
                )
            elif days <= 60:
                print(
                    "{:<25} {:<15} {:<15} {:<16}".format(
                        license["type"], "", license["quantity"], ""
                    )
                )
            elif days <= 90:
                print(
                    "{:<25} {:<15} {:<15} {:<16}".format(
                        license["type"], "", "", license["quantity"]
                    )
                )
    print("\n\n")

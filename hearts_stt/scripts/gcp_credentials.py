# Filename: gcp_credentials.py
# Created : 15 Aug 2017
# Author  : Derek Ripper
# Purpose : Contains 2 sets of GCP(google cloud platform) credentials using 2
#           independent "google service accounts".
#           Set up to falcilitate use of google "cloud speech recogintion API"
#           Used by s2t.py

def gcp_credentials(keyowner): 

   if keyowner == "User1" :
	   credentials = r"""{
	  "type": "service_account",
	  "project_id": "gcp-sr",
	  "private_key_id": " ",
	  "private_key": "",
	  "client_email": "",
	  "client_id": "",
	  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
	  "token_uri": "https://accounts.google.com/o/oauth2/token",
	  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
	  "client_x509_cert_url": ""
	}
	"""
   elif keyowner == "User2" :
	   credentials = r"""{
	  "type": "service_account",
	  "project_id": "gcp-sr",
	  "private_key_id": " ",
	  "private_key": "",
	  "client_email": "",
	  "client_id": "",
	  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
	  "token_uri": "https://accounts.google.com/o/oauth2/token",
	  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
	  "client_x509_cert_url": ""
	}
	"""
   return credentials  

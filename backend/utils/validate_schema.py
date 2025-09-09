import requests
from jsonschema import validate

def validate_json_against_schema(json_string, schema_url):
	"""
	Validate a JSON string against a JSON schema from a URL.
	Returns True if valid, raises ValidationError if not.
	"""
	# Load the JSON data
	data = json_string

	# Fetch the schema
	response = requests.get(schema_url)
	response.raise_for_status()
	schema = response.json()

	# Validate
	validate(instance=data, schema=schema)
	return True

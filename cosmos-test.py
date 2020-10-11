############################################
# Simple upload test into Azure Cosmos DB
# 


# resources
# https://towardsdatascience.com/python-azure-cosmos-db-f212c9a8a0e6

# packages
import pandas as pd
import json
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import azure.cosmos.documents as documents
import azure.cosmos.http_constants as http_constants


print("packages imported successfully")

# create config object (can be improved later)
config = {
    "endpoint": "https://flaskappcosmosjlh.documents.azure.com:443/",
    "primarykey": "yOpiScHLt55Phu4tdLshCl6OQkuiutfPgFPPlTkMRFHU7flcNFFvXMtDdnMWUlClZmjwzMvbgPjgDxoogvY6lw=="
}

# create client object
client = cosmos_client.CosmosClient(
    config['endpoint'],
    auth={"masterKey":config['primarykey']}
)

# define database and container name
database_name = 'test'
container_name = 'test_coll'

# creates a databse if the name does not exist
try:
    database = client.CreateDatabase({
        'id': database_name
    })
    print("Database does not exist, creating now.")
# if database exists, read database
except errors.HTTPFailure:
    database = client.ReadDatabase("dbs/" + database_name)
    print("Database found, did not create.")

# create database link
database_link = 'dbs/' + database_name

# define container defintion
container_definition = {
    'id': container_name,
    'partitionKey': {
        'paths': ['/location'],
        'kind': documents.PartitionKind.Hash
    }
}

# create a container if the container name does not exist
try:
    container = client.CreateContainer(
        database_link = database_link,
        collection= container_definition,
        options={'offerThroughput': 400}
    )
    print("Contianer does not exist, creating now.")
# if container exists, read container
except errors.HTTPFailure as e:
    if e.status_code == http_constants.StatusCodes.CONFLICT:
        print("Container found, did not create.")
        container = client.ReadContainer("dbs/" + database['id'] + "/colls/" + container_definition['id'])
    else:
        raise e

# connection link string - needs further research, can't find documentation
collection_link = 'dbs/' + database_name + '/colls/' + container['id']


# example of JSON upload
client.UpsertItem(
    collection_link,
    {
    "id": "2",
    "name": "Luke",
    "location": "Colorado"
})

print("upload successful")


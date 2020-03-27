from ocean_utils.utils.utilities import get_timestamp


def get_metadata_example():
    metadata = {
      "main": {
        "type": "dataset",
        "name": "Auto rental data",
        "dateCreated": "2020-03-13T10:17:09",
        "author": "Mark",
        "license": "CC0: Public Domain Dedication",
        "price": "0",
        "files": [
          {
            "contentType": "text/plain",
            "contentLength": "525047",
            "compression": "plain",
            "index": 0,
            "url": "ipfs://QmbMLrxJTnKJfgY72YasaXr49JxjzfAbrbppfnCgPWFFAP/sample_1000.csv"
          }
        ],
        "datePublished": "2020-03-13T10:24:05"
      },
      "additionalInformation": {
        "description": "Rental car data from several companies and different car models during 2016 and 2017. The data includes the rental transaction in addition to dates and start/end locations.",
        "copyrightHolder": "Mark",
        "categories": ["Transportation"]
      }
    }
    metadata['main']['dateCreated'] = get_timestamp()
    return metadata


def get_algorithm_example():
    return '''
import json
from pathlib import Path
import os
import logging
import pandas as pd

# %% Paths
path_input = Path(os.environ.get("INPUTS", "/data/inputs"))
path_output = Path(os.environ.get("OUTPUTS", "/data/outputs"))
path_logs = Path(os.environ.get("LOGS", "/data/logs"))
dids = json.loads(os.environ.get("DIDS", '[]'))
assert dids, f'no DIDS are defined, cannot continue with the algorithm'

did = dids[0]
input_files_path = Path(os.path.join(path_input, did))
input_files = list(input_files_path.iterdir())
first_input = input_files.pop()
# assert len(input_files) == 1, "Currently, only 1 input file is supported."
path_input_file = first_input
print(f'got input file: {path_input_file}, {did}, {input_files}')
path_output_file = path_output / 'summary.csv'

# %% Check all paths
assert path_input_file.exists(), "Can't find required mounted path: {}".format(path_input_file)
assert path_input_file.is_file() | path_input_file.is_symlink(), "{} must be a file.".format(path_input_file)
assert path_output.exists(), "Can't find required mounted path: {}".format(path_output)
# assert path_logs.exists(), "Can't find required mounted path: {}".format(path_output)
print(f"Selected input file: {path_input_file} {os.path.getsize(path_input_file)/1000/1000} MB")
print(f"Target output folder: {path_output}")

# %% Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', handlers=[logging.StreamHandler()])

logging.info("Starting logging")

# %% Load data
logging.debug("Loading {}".format(path_input_file))
with open(path_input_file, 'rb') as fh:
    df = pd.read_csv(fh)

logging.debug("Loaded {} records into DataFrame".format(len(df)))

summary = df.describe()
logging.debug("Built summary of records.")
summary.to_csv(path_output_file)
logging.debug("Wrote results to {}".format(path_output_file))

logging.debug("FINISHED ALGORITHM EXECUTION")
'''


def get_ddo_example():
    return {
        "@context": "https://w3id.org/future-method/v1",
        "id": "did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
        "publicKey": [
        {
          "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-1",
          "type": "RsaVerificationKey2018",
          "owner": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
          "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----"
        },
        {
          "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-2",
          "type": "Ed25519VerificationKey2018",
          "owner": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
          "publicKeyBase58": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
        },
        {
          "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-3",
          "type": "RsaPublicKeyExchangeKey2018",
          "owner": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
          "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----"
        }
        ],
        "authentication": [
        {
          "type": "RsaSignatureAuthentication2018",
          "publicKey": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-1"
        },
        {
          "type": "ieee2410Authentication2018",
          "publicKey": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2#keys-2"
        }
        ],
        "service": [
            {
              "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
              "type": "access",
              "serviceEndpoint": "http://mybrizo.org/api/v1/brizo/services/consume?pubKey=${pubKey}&serviceId={serviceId}&url={url}",
              "templateId": "0x1234",
              "attributes": {
                "main": {
                  "name": "dataAssetAccessServiceAgreement",
                  "creator": "",
                  "datePublished": "2019-02-08T08:13:49Z",
                  "price": "10",
                  "timeout": 36000
                },
                "additionalInformation": {
                  "description": ""
                },
                "serviceAgreementTemplate": {
                  "contractName": "EscrowAccessSecretStoreTemplate",
                  "events": [
                    {
                      "name": "AgreementCreated",
                      "actorType": "consumer",
                      "handler": {
                        "moduleName": "escrowAccessSecretStoreTemplate",
                        "functionName": "fulfillLockRewardCondition",
                        "version": "0.1"
                      }
                    }
                  ],
                  "fulfillmentOrder": [
                    "lockReward.fulfill",
                    "accessSecretStore.fulfill",
                    "escrowReward.fulfill"
                  ],
                  "conditionDependency": {
                    "lockReward": [],
                    "grantSecretStoreAccess": [],
                    "releaseReward": [
                      "lockReward",
                      "accessSecretStore"
                    ]
                  },
                  "conditions": [
                    {
                      "name": "lockReward",
                      "timelock": 0,
                      "timeout": 0,
                      "contractName": "LockRewardCondition",
                      "functionName": "fulfill",
                      "parameters": [
                        {
                          "name": "_rewardAddress",
                          "type": "address",
                          "value": ""
                        },
                        {
                          "name": "_amount",
                          "type": "uint256",
                          "value": "1"
                        }
                      ],
                      "events": [
                        {
                          "name": "Fulfilled",
                          "actorType": "publisher",
                          "handler": {
                            "moduleName": "lockRewardCondition",
                            "functionName": "fulfillAccessSecretStoreCondition",
                            "version": "0.1"
                          }
                        }
                      ]
                    },
                    {
                      "name": "accessSecretStore",
                      "timelock": 0,
                      "timeout": 0,
                      "contractName": "AccessSecretStoreCondition",
                      "functionName": "fulfill",
                      "parameters": [
                        {
                          "name": "_documentId",
                          "type": "bytes32",
                          "value": ""
                        },
                        {
                          "name": "_grantee",
                          "type": "address",
                          "value": ""
                        }
                      ],
                      "events": [
                        {
                          "name": "Fulfilled",
                          "actorType": "publisher",
                          "handler": {
                            "moduleName": "accessSecretStore",
                            "functionName": "fulfillEscrowRewardCondition",
                            "version": "0.1"
                          }
                        },
                        {
                          "name": "TimedOut",
                          "actorType": "consumer",
                          "handler": {
                            "moduleName": "accessSecretStore",
                            "functionName": "fulfillEscrowRewardCondition",
                            "version": "0.1"
                          }
                        }
                      ]
                    },
                    {
                      "name": "escrowReward",
                      "timelock": 0,
                      "timeout": 0,
                      "contractName": "EscrowReward",
                      "functionName": "fulfill",
                      "parameters": [
                        {
                          "name": "_amount",
                          "type": "uint256",
                          "value": "1"
                        },
                        {
                          "name": "_receiver",
                          "type": "address",
                          "value": ""
                        },
                        {
                          "name": "_sender",
                          "type": "address",
                          "value": ""
                        },
                        {
                          "name": "_lockCondition",
                          "type": "bytes32",
                          "value": ""
                        },
                        {
                          "name": "_releaseCondition",
                          "type": "bytes32",
                          "value": ""
                        }
                      ],
                      "events": [
                        {
                          "name": "Fulfilled",
                          "actorType": "publisher",
                          "handler": {
                            "moduleName": "escrowRewardCondition",
                            "functionName": "verifyRewardTokens",
                            "version": "0.1"
                          }
                        }
                      ]
                    }
                  ]
                }
              }
            },
            {
              "id": "did:op:did:op:d75305ebc1617834339e64cdafb7fd542aa657c0f94dac0f4f84068f5f910ca2",
              "type": "metadata",
              "serviceEndpoint": "http://myaquarius.org/api/v1/provider/assets/metadata/{did}",
              "attributes": {
                "main": {
                  "name": "UK Weather information 2011",
                  "type": "dataset",
                  "dateCreated": "2012-10-10T17:00:000Z",
                  "author": "Met Office",
                  "license": "CC-BY",
                  "files": [
                    {
                      "url": "https://testocnfiles.blob.core.windows.net/testfiles/testzkp.zip",
                      "index": 0,
                      "encoding": "UTF-8",
                      "compression": "zip",
                      "contentLength": "",
                      "contentType": "text/csv"
                    }
                  ],
                  "price": "10"
                },
                "curation": {
                  "rating": 0.93,
                  "numVotes": 123,
                  "schema": "Binary Voting"
                },
                "additionalInformation": {
                  "description": "Weather information of UK including temperature and humidity",
                  "workExample": "423432fsd,51.509865,-0.118092,2011-01-01T10:55:11+00:00,7.2,68",
                  "updateFrequency": "yearly",
                  "inLanguage": "en",
                  "tags": ["weather", "uk", "2011", "temperature", "humidity"],
                  "links": [
                    {
                      "name": "Sample of Asset Data",
                      "type": "sample",
                      "url": "https://foo.com/sample.csv"
                    },
                    {
                      "name": "Data Format Definition",
                      "type": "format",
                      "url": "https://foo.com/sample_1.csv",
                      "AssetID": "4d517500da0acb0d65a716f61330969334630363ce4a6a9d39691026ac7908ea"}
                  ],
                  "structuredMarkup": [
                    {
                      "uri": "http://skos.um.es/unescothes/C01194/jsonld",
                      "mediaType": "application/ld+json"
                    },
                    {
                      "uri": "http://skos.um.es/unescothes/C01194/turtle",
                      "mediaType": "text/turtle"
                    }
                  ]
                }
              }
            }
        ]
    }

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

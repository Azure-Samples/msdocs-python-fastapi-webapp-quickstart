from typing import Union
from enum import Enum
import json
import os
import requests
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Parameters(BaseModel):
    hexstring: str
    maxfeerate:  Union[str, None] = None


class BlockChainName(str, Enum):
    BitcoinTest = "BitcoinTest"
    Bitcoin = "Bitcoin"
    Ethereum = "Ethereum"


app = FastAPI()
load_dotenv()


@app.post("/sendrawtransaction/")
async def send_raw_transaction(Parameters: Parameters):
    url = os.getenv('BITCOIN_TEST_END_POINT_URL')
    payload = json.dumps({
        "method": "sendrawtransaction",
        "params": [
            Parameters.hexstring
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


@app.get("/chains")
async def get_chains():
    with open('./chainRegistry.json', 'r') as f:

        chains = json.load(f)

    return chains


@app.get("/get_address/{address}")
async def get_address_from_block_chain(address: str):
    url = os.getenv('BITCOIN_TEST_END_POINT_URL')

    payload = json.dumps({
        "method": "bb_getaddress",
        "params": [
            address,
            {
                "page": 1,
                "size": 1000,
                "fromHeight": 0,
                "details": "txs"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


@app.get("/get_utxos/{address}")
async def get_utxos_from_block_chain(address: str):
    url = os.getenv('BITCOIN_TEST_END_POINT_URL')

    payload = json.dumps({
        "method": "bb_getutxos",
        "params": [
            address,
            {
                "confirmed": True
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


@app.get("/get_tx/{txid}")
async def get_tx_from_block_chain(txid: str):
    url = os.getenv('BITCOIN_TEST_END_POINT_URL')

    payload = json.dumps({
        "method": "bb_gettx",
        "params": [
            txid
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


@app.get("/decoderawtransaction/{hexstring}")
async def decoderawtransaction(hexstring: str):
    url = os.getenv('BITCOIN_TEST_END_POINT_URL')

    payload = json.dumps({
        "method": "decoderawtransaction",
        "params": [
            hexstring
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


@app.get("/testmempoolaccept/{rawtxs}")
async def testmempoolaccept(rawtxs: str):
    url = os.getenv('BITCOIN_TEST_END_POINT_URL')

    payload = json.dumps({
        "method": "testmempoolaccept",
        "params": [
            rawtxs
        ]
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


@app.get("/estimatesmartfee/{conf_target}")
async def estimate_smart_fee(conf_target: int):
    url = os.getenv('BITCOIN_TEST_END_POINT_URL')

    payload = json.dumps({
        "method": "estimatesmartfee",
        "params": [
            conf_target
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


@app.get("/wallet/{block_chain_name}/{xpub}")
async def get_wallet(block_chain_name: BlockChainName, xpub: str):

    wallet = await get_wallet_from_block_chain(block_chain_name, xpub)

    return wallet


async def get_wallet_from_block_chain(block_chain_name: str, xpub: str):

    block_chain_url = get_block_chain_url_end_point(block_chain_name)

    wallet_request_payload = get_wallet_request_payload(
        block_chain_name, xpub)

    headers = {'Content-Type': 'application/json'}

    wallet_from_block_chain = requests.request(
        "POST", block_chain_url, headers=headers, data=wallet_request_payload)

    wallet = add_the_required_key_value_pairs_to_the_JSON_object(
        json.loads(wallet_from_block_chain.text))

    return wallet


def get_block_chain_url_end_point(block_chain_name: str):
    block_chain_endPoints = {
        'BitcoinTest': os.getenv('BITCOIN_TEST_END_POINT_URL'),
        'Bitcoin': os.getenv('BITCOIN_END_POINT_URL'),
        'Ethereum': os.getenv('ETHEREUM_END_POINT_URL')
    }
    return block_chain_endPoints[block_chain_name]


def get_wallet_request_payload(block_chain_name: str, xpub: str):
    wallet_request_payloads = {
        'BitcoinTest': json.dumps({
            "method": "bb_getxpub",
            "params": [
                f'pkh({xpub})',
                {
                    "page": 1,
                    "size": 1000,
                    "fromHeight": 0,
                    "details": "txid"
                }
            ]
        }),
        'Bitcoin': json.dumps({"method": "getblockchaininfo"}),
        'Ethereum': json.dumps({"method": "getblockchaininfo"})
    }
    return wallet_request_payloads[block_chain_name]


def add_the_required_key_value_pairs_to_the_JSON_object(response_from_blockChain):

    response_from_blockChain['id'] = '1'
    response_from_blockChain['name'] = 'BitcoinTest'
    response_from_blockChain['symbol'] = 'BTC'
    response_from_blockChain['logo'] = 'https://raw.githubusercontent.com/Oxchanger/crypto-logo/5aed02c4c539c4161073b903590945733b0c747b/btc.svg'
    response_from_blockChain['explorerUrl'] = 'some_explorerUrl'

    return response_from_blockChain


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

from flask import Flask, jsonify, request, session 
from flask_restful import Resource, Api
from pymongo import MongoClient
import requests
from web3 import Web3

rpc = "http://127.0.0.1:8545"

web3 = Web3(Web3.HTTPProvider(rpc))

abi = '[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"cp","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"cd","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"allpatients","outputs":[{"name":"name","type":"string"},{"name":"age","type":"uint256"},{"name":"bloodgroup","type":"string"},{"name":"ndoc","type":"uint256"},{"name":"npres","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"alldoctors","outputs":[{"name":"name","type":"string"},{"name":"hospital","type":"string"},{"name":"npat","type":"uint256"},{"name":"specialization","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"pid","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"hospital","type":"string"},{"name":"specialization","type":"string"}],"name":"initdoc","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"age","type":"uint256"},{"name":"bloodgroup","type":"string"}],"name":"initpat","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"pattt","type":"uint256"},{"name":"n","type":"string"},{"name":"c","type":"string"},{"name":"dos","type":"uint256"},{"name":"u","type":"string"},{"name":"pe","type":"string"},{"name":"dur","type":"uint256"}],"name":"addPrescriptions","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

contract_addr = "0xe0641afa5d665cA2c737bCA48AD7d5f1dba822CD"

contract = web3.eth.contract(address=contract_addr, abi=abi)

PATH = "http://127.0.0.1:5000/"
app = Flask(__name__)
app.secret_key = 'i love white chocolate'
api = Api(app)

class register_patient(Resource):
    def post(self):
        req = eval(request.data.decode())
        public_key = req["public"]
        private_key = req["private"]
        transaction  = contract.functions.initpat(req["name"],req["age"],req["blood_group"]).buildTransaction()
        transaction['nonce'] = web3.eth.getTransactionCount(public_key)
        signed_tx = web3.eth.account.signTransaction(transaction, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return str(tx_hash),200

api.add_resource(register_patient, '/register_patient')

if __name__ == '__main__':
    app.run(debug=True)


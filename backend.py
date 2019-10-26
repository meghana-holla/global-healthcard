from flask import Flask, jsonify, request, session 
from flask_restful import Resource, Api
from pymongo import MongoClient
import requests
from web3 import Web3

rpc = "http://127.0.0.1:8545"

web3 = Web3(Web3.HTTPProvider(rpc))

abi = '[{"constant":true,"inputs":[],"name":"get_pres_return_value","outputs":[{"name":"name","type":"string"},{"name":"company","type":"string"},{"name":"dose","type":"uint256"},{"name":"unit","type":"string"},{"name":"period","type":"string"},{"name":"duration","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"cp","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"cd","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"allpatients","outputs":[{"name":"name","type":"string"},{"name":"age","type":"uint256"},{"name":"bloodgroup","type":"string"},{"name":"ndoc","type":"uint256"},{"name":"npres","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"get_pat_return_value","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"get_doc_return_value","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"alldoctors","outputs":[{"name":"name","type":"string"},{"name":"hospital","type":"string"},{"name":"npat","type":"uint256"},{"name":"specialization","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"pid","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"hospital","type":"string"},{"name":"specialization","type":"string"}],"name":"initdoc","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"name","type":"string"},{"name":"age","type":"uint256"},{"name":"bloodgroup","type":"string"}],"name":"initpat","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name":"getpat","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name":"getdoc","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name":"getpres","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"pat_id","type":"uint256"},{"name":"name","type":"string"},{"name":"company","type":"string"},{"name":"dose","type":"uint256"},{"name":"unit","type":"string"},{"name":"period","type":"string"},{"name":"duration","type":"uint256"}],"name":"addPrescriptions","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

contract_addr = "0x8fDd21C593c5693788E0248b4C86bB66375f8dA7"

contract = web3.eth.contract(address=contract_addr, abi=abi)

PATH = "http://127.0.0.1:5000/"
app = Flask(__name__)
app.secret_key = 'i love white chocolate'
api = Api(app)

class register_doctor(Resource):
    def post(self):
        req = eval(request.data.decode())

        public_key = req["public"]
        private_key = req["private"]
        transaction  = contract.functions.initdoc(
            req["name"],
            req["hospital"],
            req['specialization']).buildTransaction()
        transaction['nonce'] = web3.eth.getTransactionCount(public_key)

        signed_tx = web3.eth.account.signTransaction(transaction, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return str(tx_hash),200
        
api.add_resource(register_doctor, '/register_doctor')

class add_prescription(Resource):
    def post(self):
        req = eval(request.data.decode())

        public_key = req["public"]
        private_key = req["private"]

        transaction  = contract.functions.addPrescriptions(
            req["pat_id"],
            req["name"], 
            req['company'], 
            req["dose"], 
            req["unit"], 
            req["period"], 
            req["duration"]).buildTransaction()
        transaction['nonce'] = web3.eth.getTransactionCount(public_key)

        signed_tx = web3.eth.account.signTransaction(transaction, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return str(tx_hash),200

api.add_resource(add_prescription, '/add_prescription')

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

class get_patients(Resource):
    def get(self):
        req = eval(request.data.decode())
        public_key = req["public"]
        private_key = req["private"]
        n = contract.caller().alldoctors(public_key)[2];
        print(n)
        ret = []
        for i in range(n):
            transaction  = contract.functions.getpat(i).buildTransaction()
            transaction['nonce'] = web3.eth.getTransactionCount(public_key)
            transaction['gas'] = 3000000
            signed_tx = web3.eth.account.signTransaction(transaction, private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            retVal = contract.caller().get_pat_return_value();
            ret.append(contract.caller().allpatients(str(retVal)))
        return ret
api.add_resource(get_patients, '/get_patients')

class get_doctor(Resource):
    def get(self):
        req = eval(request.data.decode())
        public_key = req["public"]
        private_key = req["private"]
        n = contract.caller().allpatients(public_key)[3];
        print(n)
        ret = []
        for i in range(n):
            transaction  = contract.functions.getdoc(i).buildTransaction()
            transaction['nonce'] = web3.eth.getTransactionCount(public_key)
            transaction['gas'] = 3000000
            signed_tx = web3.eth.account.signTransaction(transaction, private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            retVal = contract.caller().get_doc_return_value();
            ret.append(contract.caller().alldoctors(str(retVal)))
        return ret
api.add_resource(get_doctor, '/get_doctor')

class get_pres(Resource):
    def get(self):
        req = eval(request.data.decode())
        public_key = req["public"]
        private_key = req["private"]
        n = contract.caller().allpatients(public_key)[4];
        ret = []
        for i in range(n):
            transaction  = contract.functions.getpres(i).buildTransaction()
            transaction['nonce'] = web3.eth.getTransactionCount(public_key)
            transaction['gas'] = 3000000
            signed_tx = web3.eth.account.signTransaction(transaction, private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            retVal = contract.caller().get_pres_return_value();
            ret.append(retVal)
        return ret
api.add_resource(get_pres, '/get_pres')

if __name__ == '__main__':
    app.run(debug=True)


from web3 import Web3, EthereumTesterProvider
import json
import time
import tkinter
from tkinter import ttk
import tkinter.messagebox as msgbox

global contractInstance;
address = '0xDAef0D76b3bE27D69da266364Ebd47311CeB6Ac9'
myAbi = """[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "bidTime",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "myBenificiary",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "myhighestBid",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "address",
				"name": "winner",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "AuctionEnded",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "address",
				"name": "bidder",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "HighestBidIncreased",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "auctionEnd",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "auctionEndTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "auctionEndWithDraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "benificiary",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "bid",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "ended",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBalance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getTimeStamp",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "highestBid",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "highestBider",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "isWithdraw",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "pendingReturns",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "withdraw",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]"""

myBytecode ="60806040523480156200001157600080fd5b506040516200136438038062001364833981810160405281019062000037919062000141565b816000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555082426200008591906200019d565b6001819055506000600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550806003819055506000600560006101000a81548160ff0219169083151502179055506000600560016101000a81548160ff021916908315150217905550505050620002a0565b60008151905062000124816200026c565b92915050565b6000815190506200013b8162000286565b92915050565b6000806000606084860312156200015d576200015c62000267565b5b60006200016d868287016200012a565b9350506020620001808682870162000113565b925050604062000193868287016200012a565b9150509250925092565b6000620001aa826200022e565b9150620001b7836200022e565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff03821115620001ef57620001ee62000238565b5b828201905092915050565b600062000207826200020e565b9050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600080fd5b6200027781620001fa565b81146200028357600080fd5b50565b62000291816200022e565b81146200029d57600080fd5b50565b6110b480620002b06000396000f3fe6080604052600436106100c25760003560e01c80632a24f46c1161007f5780636b57707e116100595780636b57707e146101ff578063d57bde791461022a578063da235b2214610255578063dbae172c14610280576100c2565b80632a24f46c146101a65780633ccfd60b146101bd5780634b449cba146101d4576100c2565b80630405c357146100c757806306d6c19d146100f257806312065fe01461010957806312fa6feb146101345780631998aeef1461015f57806326b387bb14610169575b600080fd5b3480156100d357600080fd5b506100dc6102ab565b6040516100e99190610c0d565b60405180910390f35b3480156100fe57600080fd5b506101076102cf565b005b34801561011557600080fd5b5061011e6104e6565b60405161012b9190610d8c565b60405180910390f35b34801561014057600080fd5b506101496104ee565b6040516101569190610c51565b60405180910390f35b610167610501565b005b34801561017557600080fd5b50610190600480360381019061018b9190610a4e565b610787565b60405161019d9190610d8c565b60405180910390f35b3480156101b257600080fd5b506101bb61079f565b005b3480156101c957600080fd5b506101d2610800565b005b3480156101e057600080fd5b506101e96109ec565b6040516101f69190610d8c565b60405180910390f35b34801561020b57600080fd5b506102146109f2565b6040516102219190610bf2565b60405180910390f35b34801561023657600080fd5b5061023f610a18565b60405161024c9190610d8c565b60405180910390f35b34801561026157600080fd5b5061026a610a1e565b6040516102779190610d8c565b60405180910390f35b34801561028c57600080fd5b50610295610a26565b6040516102a29190610c51565b60405180910390f35b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161461035d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161035490610d0c565b60405180910390fd5b60015442116103a1576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161039890610cac565b60405180910390fd5b60001515600560019054906101000a900460ff161515146103f7576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016103ee90610ccc565b60405180910390fd5b6001600560016101000a81548160ff02191690831515021790555060008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc600160035461045b9190610e0e565b9081150290604051600060405180830381858888f19350505050158015610486573d6000803e3d6000fd5b507fdaec4582d5d9595688c8c98545fdd1c696d41c6aeaeb636737e84ed2f5c00eda600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff166003546040516104dc929190610c28565b60405180910390a1565b600047905090565b600560009054906101000a900460ff1681565b600154421115610546576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161053d90610cec565b60405180910390fd5b60001515600560009054906101000a900460ff1615151461059c576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161059390610d6c565b60405180910390fd5b600034116105df576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016105d690610c6c565b60405180910390fd5b60035434600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205461062d9190610db8565b1161066d576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161066490610c8c565b60405180910390fd5b34600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060008282546106bc9190610db8565b9250508190555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546003819055507ff4757a49b326036464bec6fe419a4ae38c8a02ce3e68bf0809674f6aab8ad3003360035460405161077d929190610c28565b60405180910390a1565b60046020528060005260406000206000915090505481565b60015442116107e3576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016107da90610cac565b60405180910390fd5b6001600560006101000a81548160ff021916908315150217905550565b6000600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205411610882576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161087990610d2c565b60405180910390fd5b3373ffffffffffffffffffffffffffffffffffffffff16600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff161415610913576040517f08c379a000000000000000000000000000000000000000000000000000000000815260040161090a90610d4c565b60405180910390fd5b3373ffffffffffffffffffffffffffffffffffffffff166108fc6001600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546109799190610e0e565b9081150290604051600060405180830381858888f193505050501580156109a4573d6000803e3d6000fd5b506000600460003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081905550565b60015481565b600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60035481565b600042905090565b600560019054906101000a900460ff1681565b600081359050610a4881611067565b92915050565b600060208284031215610a6457610a63610ef1565b5b6000610a7284828501610a39565b91505092915050565b610a8481610e7a565b82525050565b610a9381610e68565b82525050565b610aa281610e8c565b82525050565b6000610ab5600c83610da7565b9150610ac082610ef6565b602082019050919050565b6000610ad8600783610da7565b9150610ae382610f1f565b602082019050919050565b6000610afb602083610da7565b9150610b0682610f48565b602082019050919050565b6000610b1e601083610da7565b9150610b2982610f71565b602082019050919050565b6000610b41600f83610da7565b9150610b4c82610f9a565b602082019050919050565b6000610b64601083610da7565b9150610b6f82610fc3565b602082019050919050565b6000610b87601d83610da7565b9150610b9282610fec565b602082019050919050565b6000610baa601a83610da7565b9150610bb582611015565b602082019050919050565b6000610bcd601483610da7565b9150610bd88261103e565b602082019050919050565b610bec81610eb8565b82525050565b6000602082019050610c076000830184610a8a565b92915050565b6000602082019050610c226000830184610a7b565b92915050565b6000604082019050610c3d6000830185610a8a565b610c4a6020830184610be3565b9392505050565b6000602082019050610c666000830184610a99565b92915050565b60006020820190508181036000830152610c8581610aa8565b9050919050565b60006020820190508181036000830152610ca581610acb565b9050919050565b60006020820190508181036000830152610cc581610aee565b9050919050565b60006020820190508181036000830152610ce581610b11565b9050919050565b60006020820190508181036000830152610d0581610b34565b9050919050565b60006020820190508181036000830152610d2581610b57565b9050919050565b60006020820190508181036000830152610d4581610b7a565b9050919050565b60006020820190508181036000830152610d6581610b9d565b9050919050565b60006020820190508181036000830152610d8581610bc0565b9050919050565b6000602082019050610da16000830184610be3565b92915050565b600082825260208201905092915050565b6000610dc382610eb8565b9150610dce83610eb8565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff03821115610e0357610e02610ec2565b5b828201905092915050565b6000610e1982610eb8565b9150610e2483610eb8565b9250817fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0483118215151615610e5d57610e5c610ec2565b5b828202905092915050565b6000610e7382610e98565b9050919050565b6000610e8582610e98565b9050919050565b60008115159050919050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b600080fd5b7f6d73672e76616c7565203e300000000000000000000000000000000000000000600082015250565b7f6f76657262696400000000000000000000000000000000000000000000000000600082015250565b7f626c6f636b2e74696d657374616d70203e2061756374696f6e456e6454696d65600082015250565b7f646964206e6f7420776974686472617700000000000000000000000000000000600082015250565b7f757064617465206e6f772074696d650000000000000000000000000000000000600082015250565b7f6f6e6c792062656e696669636961727900000000000000000000000000000000600082015250565b7f70656e64696e6752657475726e735b6d73672e73656e6465725d203e30000000600082015250565b7f68696768657374426964657220213d206d73672e73656e646572000000000000600082015250565b7f626964696e6720666c616720697320656e646564000000000000000000000000600082015250565b61107081610e68565b811461107b57600080fd5b5056fea264697066735822122045c888c0404e5e68ff9cadf25cb5d2c91a641d81527002dc73e00acf78dcc49664736f6c63430008070033";


def storeLocalContractAddress(address):
	with open("LocalContractAddress.txt","w") as f:
		f.write(address);


def server():

	#连接web3
	w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
	#测试connect
	if(w3.isConnected() == True):
		print("true");
	else:
		print("false");
		return;
	
	addressTemp =address;
	#创建合约 并保存合约地址
	contractInstance = w3.eth.contract(address=addressTemp, abi=myAbi,bytecode = myBytecode);
	
	#进行构造函数 #uint bidTime ,address payable myBenificiary,uint myhighestBid
	option = {'from':addressTemp, 'gas':3000000};
	bidTime =300;#e2.get();#5min
	myBenificiary = addressTemp;
	myhighestBid = 0;#e3.get();
	txHash = contractInstance.constructor(bidTime,myBenificiary,myhighestBid).transact(option);
	receiptCreate = w3.eth.waitForTransactionReceipt(txHash);
	
	storeLocalContractAddress(receiptCreate.contractAddress);
	
	msgbox.showinfo('成功', '发布成功');

def getAuctionInfo():
	global contractInstance;
	initContractInstance();
	#获取合约值，然后赋值
	#labelAddressShow['text'] = e1.get();
	#获取账户余额
	w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
	if(w3.isConnected() == True):
		print("true");
	else:
		print("false");
		return;	
	labelBalanceShow['text'] = w3.eth.getBalance(e1.get());
	#获取结束时间
	labelAuctionEndTimeShow['text'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(contractInstance.functions.auctionEndTime().call()));
	#获取拍卖最高价格
	labelHighPriceShow['text'] = contractInstance.functions.highestBid().call();
	#获取拍卖最高地址
	labelHighAddressShow['text'] = contractInstance.functions.highestBider().call();
	#获取合约剩余的余额
	labelContractBalanceShow['text'] = contractInstance.functions.getBalance().call();
	
def initContractInstance():
	global contractInstance;
	#连接web3
	w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
	#测试connect
	if(w3.isConnected() == True):
		print("true");
	else:
		print("false");
		return;
	#读取创建好的合约
	contractInstance = w3.eth.contract(address=readLocalContractAddress(), abi=myAbi,bytecode = myBytecode);

def readLocalContractAddress():
	with open("LocalContractAddress.txt","r") as f:
		return f.readlines()[0];
		
		
def getWinner():
	global contractInstance;
	initContractInstance();
	try:
		contractInstance.functions.auctionEnd().call();
		#获取合约剩余的余额
		labelWinnerShow['text'] = contractInstance.functions.highestBider().call();
		labelWinnerPriceShow['text'] = contractInstance.functions.highestBid().call();
	except BaseException as e:
		print(e);
		msgbox.showinfo('异常', '拍卖还没结束');
		return;
	msgbox.showinfo('成功', '拍卖结束，winner成功');

#取款
def withdraw():
	try:
		option = {'from':contractInstance.functions.benificiary().call(), 'gas':1000000};
		contractInstance.functions.auctionEndWithDraw().transact(transaction = option);
	except BaseException as e:
		print(e);
		msgbox.showinfo('异常', '取款不成功');
		return;
	msgbox.showinfo('成功', '取款成功');
	
#这里要处理下成为单数据集
top = tkinter.Tk()

top.geometry("800x600+100+50")
top.title("拍卖 server端")
#==========================按钮========================
b1 = tkinter.Button(top, text ="发布拍卖合约", command = server);
b1.grid(row=3, column=0,padx=0,pady=10,ipadx= 5);


label1 = ttk.Label(top,text="发布人地址：",width = 16);
label1.grid(row=0, column=0,padx=10,pady=10)
e1 = tkinter.Entry(width = 50);
e1.grid(row=0, column=1,padx=0,pady=10,ipadx= 5)
labelUnit1 = ttk.Label(top,text="单位",width = 16);
labelUnit1.grid(row=0, column=2,padx=10,pady=10);

	

label2 = ttk.Label(top,text="拍卖时间：",width = 16);
label2.grid(row=1, column=0,padx=10,pady=10)
e2 = tkinter.Entry(width = 50);
e2.grid(row=1, column=1,padx=0,pady=10,ipadx= 5)
labelUnit2 = ttk.Label(top,text="单位(s)",width = 16);
labelUnit2.grid(row=1, column=2,padx=10,pady=10);



label3 = ttk.Label(top,text="底价：",width = 16);
label3.grid(row=2, column=0,padx=10,pady=10)
e3 = tkinter.Entry(width = 50);
e3.grid(row=2, column=1,padx=0,pady=10,ipadx= 5)
labelUnit3 = ttk.Label(top,text="单位(wei)",width = 16);
labelUnit3.grid(row=2, column=2,padx=10,pady=10);

#分割线
labelLine1 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 16);
labelLine1.grid(row=4, column=0,padx=0,pady=0);
labelLine2 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 50);
labelLine2.grid(row=4, column=1,padx=0,pady=0);
labelLine3 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 16);
labelLine3.grid(row=4, column=2,padx=0,pady=0);
labelLine4 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 16);
labelLine4.grid(row=4, column=3,padx=0,pady=0);

#查看个人余额
labelBalance = ttk.Label(top,text="余额：",width = 16);
labelBalance.grid(row=5, column=0,padx=10,pady=10);
labelBalanceShow = ttk.Label(top,text="0",width = 50);
labelBalanceShow.grid(row=5, column=1,padx=10,pady=10);
labelBalanceUnit = ttk.Label(top,text="wei",width = 16);
labelBalanceUnit.grid(row=5, column=2,padx=10,pady=10);
b1 = tkinter.Button(top, text ="查看拍卖信息", command = getAuctionInfo);
b1.grid(row=5, column=3,padx=0,pady=10,ipadx= 5);
#查看拍卖结束时间
labelAuctionEndTime = ttk.Label(top,text="结束时间：",width = 16);
labelAuctionEndTime.grid(row=6, column=0,padx=10,pady=10);
labelAuctionEndTimeShow = ttk.Label(top,text="0",width = 50);
labelAuctionEndTimeShow.grid(row=6, column=1,padx=10,pady=10);
labelAuctionEndTimeUnit = ttk.Label(top,text="单位",width = 16);
labelAuctionEndTimeUnit.grid(row=6, column=2,padx=10,pady=10);
#查看最高价格
labelHighPrice = ttk.Label(top,text="最高价格：",width = 16);
labelHighPrice.grid(row=7, column=0,padx=10,pady=10);
labelHighPriceShow = ttk.Label(top,text="0",width = 50);
labelHighPriceShow.grid(row=7, column=1,padx=10,pady=10);
labelHighPriceUnit = ttk.Label(top,text="wei",width = 16);
labelHighPriceUnit.grid(row=7, column=2,padx=10,pady=10);
#最高价格地址
labelHighAddress = ttk.Label(top,text="最高价格地址：",width = 16);
labelHighAddress.grid(row=8, column=0,padx=10,pady=10);
labelHighAddressShow = ttk.Label(top,text="0",width = 50);
labelHighAddressShow.grid(row=8, column=1,padx=10,pady=10);
#查看合约剩余的余额
labelContractBalance = ttk.Label(top,text="合约余额：",width = 16);
labelContractBalance.grid(row=9, column=0,padx=10,pady=10);
labelContractBalanceShow = ttk.Label(top,text="0",width = 50);
labelContractBalanceShow.grid(row=9, column=1,padx=10,pady=10);
labelContractBalanceUnit = ttk.Label(top,text="wei",width = 16);
labelContractBalanceUnit.grid(row=9, column=2,padx=10,pady=10);

#分割线
labelLine1 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 16);
labelLine1.grid(row=10, column=0,padx=0,pady=0);
labelLine2 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 50);
labelLine2.grid(row=10, column=1,padx=0,pady=0);
labelLine3 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 16);
labelLine3.grid(row=10, column=2,padx=0,pady=0);
labelLine4 = ttk.Label(top,text="------------------------------------------------------------------------------------",width = 16);
labelLine4.grid(row=10, column=3,padx=0,pady=0);

#查看最高竞拍人 拍卖结束
labelWinner = ttk.Label(top,text="winner：",width = 16);
labelWinner.grid(row=11, column=0,padx=10,pady=10);
labelWinnerShow = ttk.Label(top,text="0",width = 50);
labelWinnerShow.grid(row=11, column=1,padx=10,pady=10);
buttonWithdraw = tkinter.Button(top, text ="查看winner", command = getWinner);
buttonWithdraw.grid(row=11, column=3,padx=0,pady=10,ipadx= 5);
#winner最高价
labelWinnerPrice = ttk.Label(top,text="winner最高价：",width = 16);
labelWinnerPrice.grid(row=12, column=0,padx=10,pady=10);
labelWinnerPriceShow = ttk.Label(top,text="0",width = 50);
labelWinnerPriceShow.grid(row=12, column=1,padx=10,pady=10);
#取款
buttonWithdraw = tkinter.Button(top, text ="取款", command = withdraw);
buttonWithdraw.grid(row=12, column=3,padx=0,pady=10,ipadx= 5);

top.mainloop()










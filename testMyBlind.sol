// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;
//简单拍卖系统
contract SimpleAuction {
    address payable public benificiary;//受益人
    uint public auctionEndTime;//拍卖结束时间
    address public highestBider;//当前出家最高人
    uint public highestBid;//最高价格 单位wei

    mapping(address => uint) public pendingReturns;//记录返还的钱地址
    bool public ended;//拍卖是否结束标记
    bool public isWithdraw;//受益人是否已经取款

    event HighestBidIncreased(address bidder ,uint amount);
    event AuctionEnded(address winner,uint amount );

    constructor(uint bidTime ,address payable myBenificiary,uint myhighestBid){
        //初始化当前的受益人 
        benificiary = myBenificiary;
        //初始化拍卖时间
        auctionEndTime = block.timestamp +bidTime;
        //初始化当前出家最高人
        highestBider = address(0);
        //初始化底价
        highestBid = myhighestBid;
        //开始进行拍卖
        ended = false;
        isWithdraw = false;

    }

    //拍卖
    function bid() payable public{
        //更新现在时间
        require(block.timestamp <=auctionEndTime,"update now time");
        //检测拍卖结束标记 = false
        require(ended == false,"biding flag is ended");
        //检测msg.value是否大于0
        require(msg.value > 0,"msg.value >0");
        //检测msg.value是否大于最高价格
        require(pendingReturns[msg.sender] +msg.value > highestBid,"overbid");
        //记录mapping pendingReturns 并把钱打到这个合约上的余额
        pendingReturns[msg.sender] += msg.value;
        //记录最高价人的地址
        highestBider = msg.sender;
        highestBid = pendingReturns[msg.sender];


        emit HighestBidIncreased(msg.sender,highestBid);
    }
    
    //取款
    function withdraw() public{
        //检测已经拍卖人在记录
        require(pendingReturns[msg.sender] >0,"pendingReturns[msg.sender] >0");
        //检测拍卖人被超越
        require(highestBider != msg.sender,"highestBider != msg.sender");
        //从合约余额里面取钱
        payable(msg.sender).transfer(pendingReturns[msg.sender] *1 wei);
        //取钱后记录归0
        pendingReturns[msg.sender] = 0;
    }

    //结束得出最高出价人
    function auctionEnd() public{
        //检测拍卖时间已经结束
        require(block.timestamp > auctionEndTime,"block.timestamp > auctionEndTime");
        ended = true;

    }

    //受益者取款
    function auctionEndWithDraw() public{
        require(msg.sender == benificiary,"only benificiary");
        //检测拍卖时间已经结束
        require(block.timestamp > auctionEndTime,"block.timestamp > auctionEndTime");
        require(isWithdraw == false,"did not withdraw");
        isWithdraw = true;
        //受益人从余额拿下最高钱
        benificiary.transfer(highestBid *1 wei);
        //展示出最高价的人
        emit AuctionEnded(highestBider,highestBid);
    }
    
    //获取账户余额
    function getBalance() public view returns(uint){
        return address(this).balance;
    }

    //获取时间
    function getTimeStamp() public view returns(uint){
        return block.timestamp;
    }


}
const fs = require('fs');
const path = require('path');
const { Gateway, Wallets } = require('fabric-network');

const NETWORK_DIR = path.resolve(
    __dirname,
    '../fabric-samples/test-network'
);

const CONNECTION_PROFILE = path.join(
    NETWORK_DIR,
    'organizations/peerOrganizations/org1.example.com/connection-org1.json'
);

const CERT_PATH = path.join(
    NETWORK_DIR,
    'organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/signcerts/cert.pem'
);

const KEYSTORE_PATH = path.join(
    NETWORK_DIR,
    'organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp/keystore'
);

const CHANNEL_NAME = 'mychannel';
const CHAINCODE_NAME = 'loanledger';

let gateway;
let contract;

async function connectToFabric() {
    if (contract) {
        return contract;
    }

    const connectionProfile = JSON.parse(
        fs.readFileSync(CONNECTION_PROFILE, 'utf8')
    );

    const certificate = fs.readFileSync(CERT_PATH, 'utf8');

    const keyFile = fs.readdirSync(KEYSTORE_PATH)
        .find(file => file.endsWith('_sk'));

    if (!keyFile) {
        throw new Error('Admin private key not found');
    }

    const privateKey = fs.readFileSync(
        path.join(KEYSTORE_PATH, keyFile),
        'utf8'
    );

    const wallet = await Wallets.newInMemoryWallet();

    await wallet.put('admin', {
        credentials: {
            certificate,
            privateKey
        },
        mspId: 'Org1MSP',
        type: 'X.509'
    });

    gateway = new Gateway();

    await gateway.connect(connectionProfile, {
        wallet,
        identity: 'admin',
        discovery: {
            enabled: true,
            asLocalhost: true
        }
    });

    const network = await gateway.getNetwork(CHANNEL_NAME);

    contract = network.getContract(CHAINCODE_NAME);

    console.log('Connected to Hyperledger Fabric!');
    console.log('Channel:', CHANNEL_NAME);
    console.log('Chaincode:', CHAINCODE_NAME);

    return contract;
}

async function createLoanRecord(loan) {
    const contract = await connectToFabric();

    const result = await contract.submitTransaction(
        'CreateLoanRecord',
        String(loan.loanId || ''),
        String(loan.customerId || ''),
        String(loan.customerName || ''),
        String(loan.amount || '0'),
        String(loan.loanPurpose || ''),
        String(loan.riskLevel || ''),
        String(loan.confidence || '0'),
        String(loan.status || 'Pending'),
        String(loan.timestamp || new Date().toISOString())
    );

    return result ? result.toString() : 'Loan record created successfully';
}

async function readLoan(loanId) {
    const contract = await connectToFabric();

    const result = await contract.evaluateTransaction(
        'ReadLoan',
        loanId
    );

    return JSON.parse(result.toString());
}

async function getAllLoans() {
    const contract = await connectToFabric();

    const result = await contract.evaluateTransaction(
        'GetAllLoans'
    );

    return JSON.parse(result.toString());
}

async function updateLoanStatus(loanId, status, riskCategory, confidence) {
    const contract = await connectToFabric();

    const result = await contract.submitTransaction(
        'UpdateLoanStatus',
        loanId,
        status,
        riskCategory,
        String(confidence)
    );

    return result ? result.toString() : 'Loan status updated successfully';
}

module.exports = {
    connectToFabric,
    createLoanRecord,
    readLoan,
    getAllLoans,
    updateLoanStatus
};

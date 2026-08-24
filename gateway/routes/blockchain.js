const express = require('express');

const {
    connectToFabric,
    createLoanRecord,
    readLoan,
    getAllLoans,
    updateLoanStatus
} = require('../fabric');

const router = express.Router();


// Health check
router.get('/health', async (req, res) => {
    try {
        await connectToFabric();

        res.json({
            status: 'ok',
            blockchain: 'Hyperledger Fabric',
            channel: 'mychannel',
            chaincode: 'loanledger',
            connected: true
        });

    } catch (error) {
        console.error(error);

        res.status(500).json({
            status: 'error',
            blockchain: 'Hyperledger Fabric',
            connected: false,
            error: error.message
        });
    }
});


// Create loan
router.post('/loans', async (req, res) => {
    try {

        const {
            loanId,
            customerId,
            customerName,
            amount,
            loanPurpose,
            riskLevel,
            confidence,
            status,
            timestamp
        } = req.body;

        if (!loanId || !customerId || !amount || !riskLevel || !status) {
            return res.status(400).json({
                error: 'loanId, customerId, amount, riskLevel and status are required'
            });
        }

        const result = await createLoanRecord({
            loanId: String(loanId),
            customerId: String(customerId),
            customerName: String(customerName || ''),
            amount: String(amount),
            loanPurpose: String(loanPurpose || ''),
            riskLevel: String(riskLevel),
            confidence: String(confidence || '0'),
            status: String(status),
            timestamp: String(timestamp || new Date().toISOString())
        });

        res.status(201).json({
            message: 'Loan record stored on blockchain',
            transactionResult: result
        });

    } catch (error) {
        console.error(error);

        res.status(500).json({
            error: error.message
        });
    }
});


// Get loan
router.get('/loans/:loanId', async (req, res) => {
    try {

        const loan = await readLoan(req.params.loanId);

        res.json(loan);

    } catch (error) {
        console.error(error);

        res.status(404).json({
            error: error.message
        });
    }
});


// Get all loans
router.get('/loans', async (req, res) => {
    try {

        const loans = await getAllLoans();

        res.json(loans);

    } catch (error) {
        console.error(error);

        res.status(500).json({
            error: error.message
        });
    }
});


// Update loan status
router.put('/loans/:loanId/status', async (req, res) => {
    try {

        const {
            status,
            riskCategory,
            confidence
        } = req.body;

        if (!status) {
            return res.status(400).json({
                error: 'status is required'
            });
        }

        const result = await updateLoanStatus(
            req.params.loanId,
            status,
            riskCategory,
            confidence
        );

        res.json({
            message: 'Loan status updated on blockchain',
            transactionResult: result
        });

    } catch (error) {
        console.error(error);

        res.status(500).json({
            error: error.message
        });
    }
});


module.exports = router;
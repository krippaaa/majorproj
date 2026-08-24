require('dotenv').config();

const express = require('express');
const cors = require('cors');

const blockchainRoutes = require('./routes/blockchain');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/blockchain', blockchainRoutes);

app.get('/', (req, res) => {
    res.json({
        message: 'Loan Ledger Gateway Running'
    });
});

const PORT = 4000;

app.listen(PORT, () => {
    console.log(`Gateway running on port ${PORT}`);
});
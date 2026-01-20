require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();
const port = process.env.PORT;

if (!port) {
    throw new Error("PORT is not defined in .env file");
}

app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('QR RECEIVED', qr);
    qrcode.generate(qr, { small: true });
    console.log('Please scan the QR code above with your WhatsApp.');
});

client.on('ready', () => {
    console.log('Client is ready!');
});

console.log('Initializing WhatsApp Client...');
client.initialize();

app.post('/send', async (req, res) => {
    const { phone_number, message } = req.body;

    try {
        let cleanNumber = phone_number.replace('+', '').replace('-', '').replace(' ', '');
        let chatId = cleanNumber + '@c.us';

        console.log(`Sending message to ${chatId}: ${message}`);

        await client.sendMessage(chatId, message);
        res.json({ status: 'success', message: 'Message sent' });
    } catch (error) {
        console.error("Error sending message:", error);
        res.status(500).json({ status: 'error', message: error.toString() });
    }
});

app.listen(port, () => {
    console.log(`WhatsApp Gateway listening on port ${port}`);
});

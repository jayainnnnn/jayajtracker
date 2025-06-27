const nodemailer = require('nodemailer');
require('dotenv').config();

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT),
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

exports.sendLoginEmail = async (to, token) => {


  const verifyUrl = `${process.env.APP_BASE_URL}/verify-email/${token}`;
  console.log(`📤 Trying to send login email to ${to}`);
  const mailOptions = {
    from: `"AJ Tracker" <${process.env.SMTP_USER}>`,
    to,
    subject: 'Verify your email',
    html: `<p>Click below to verify your email:</p>
           <a href="${verifyUrl}">${verifyUrl}</a>`,
  };

  const info = await transporter.sendMail(mailOptions);
  console.log('Email sent:', info.messageId);
};

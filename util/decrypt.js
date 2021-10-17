const fs = require("fs");
const AES = require("crypto-js/aes");
const enc_utf8 = require("crypto-js/enc-utf8");

const encryptText = fs.readFileSync("encrypted/create_model.py.encrypt", {
  encoding: "utf-8",
});
const bytes = AES.decrypt(encryptText, process.env.RH_PASSWORD);
const result = bytes.toString(enc_utf8);
fs.writeFileSync("encrypted/create_model.py", result)

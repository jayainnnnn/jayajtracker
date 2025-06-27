const path = require('path');
const axios = require('axios');

const reference = require("../ref/path");
const api_path = reference.api_path
const rootdir = require('../utils/pathutil');
const { sendLoginEmail } = require('../utils/email');

exports.homeController = (req,res,next) => {
    res.render('home',{pageTitle:'home',username:req.session.user?.name});
};

exports.getlogin = (req,res,next) => {
    res.sendFile(path.join(rootdir, 'views', 'login.html'));
}

exports.postlogin = async(req,res,next) => {
        const {email, password} = req.body;
        try{
            const response = await axios.post(`${api_path}/login`,{
                email,
                password
            },{
                headers: { "Content-Type": "application/json" }
            })
            console.log(response.data)
            const {name} = response.data
            req.session.user = {
            name: name,
            email: email
            };
            await sendLoginEmail(email, name);
            res.render('home',{pageTitle:'Home',username:req.session.user?.name});
        }
        catch(error){
            res.sendFile(path.join(rootdir,'views','error.html'));
        }
}

exports.getsignup = (req,res,next) => {
    res.sendFile(path.join(rootdir,'views','signup.html'));
}

exports.postsignup = async(req,res,next) => {
    const { name, email, password, phone_number} = req.body;
    console.log(req.body)
        try{
            const response = await axios.post(`${api_path}/signup`, {
                name,
                email,
                password,
                phone_number
            }, {
                headers: { "Content-Type": "application/json" }
            });
            // res.render('home',{pageTitle:'Home',username:req.session.user?.name});
            res.sendFile(path.join(rootdir,'views','login.html'));
        }
        catch(error){
            res.sendFile(path.join(rootdir,'views','signup.html'));
        }
}

exports.getlogout = (req,res,next) => {
    try{
    req.session.destroy();
    res.render('home',{pageTitle:'home',username:null});
    }
    catch(error){
        res.sendFile(path.join(rootdir,'views','error.html'));
    }
}

exports.get404 = (req,res,next) => {
    res.sendFile(path.join(rootdir,'views','404.html'));
}

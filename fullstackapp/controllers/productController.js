// global modules
const path = require('path');
const axios = require('axios');

const reference = require("../ref/path");
const api_path = reference.api_path

const rootdir = require('../utils/pathutil');

exports.laptopRouter = async(req,res,next) => {
    if (req.session.user?.name){
        const {email,name} = req.session.user
        try{
            const response = await axios.post(`${api_path}/products`,{
                email
            },{
                headers: { "Content-Type": "application/json" }
            })
            console.log(response.data)
            res.render('producthome',{
                pageTitle:"products",
                username: req.session.user.name,
                products:response.data});
        }
        catch(error){
            res.sendFile(path.join(rootdir,'views','error.html'));
        }
    }
    else{
        res.render('home',{pageTitle:'home',username:req.session.user?.name});
    }
};

exports.postadd_product = async(req,res,next) =>{
    const {url} = req.body;
    try{
        const response = await axios.post(`${api_path}/addproduct`,{
                url,
                email: req.session.user.email
            },{
                headers: { "Content-Type": "application/json" }
            });
            console.log(user.email,url)
            return res.redirect('/producthome');
        }
    catch(error){
        console.error('Error while adding product:', error.message);
        return res.redirect('/producthome')
    }
};


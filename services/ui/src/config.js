import process from 'process';

const config = {
    // other global config variables you wish
    API: "http://aicams.ca:3020/",
    // API: "http://127.0.0.1:5000/",
    //API:    "//localhost:5000/", // use it for local debuging
};

global.config=config;
console.log(JSON.stringify(process.env, null, 2));
//alert(JSON.stringify(process.env, null, 2));
import process from 'process';

const config = {
    i18n: {
        welcome: {
            en: "Welcome",
            fa: "خوش آمدید"
        }
        // rest of your translation object
    },
    // other global config variables you wish
    API: "//"+process.env.STREAM_SERVER_IP +"/" //"//192.168.0.100:3020/",
    //API:    "//localhost:5000/", // use it for local debuging
};

global.config=config;
console.log(JSON.stringify(process.env, null, 2));
//alert(JSON.stringify(process.env, null, 2));
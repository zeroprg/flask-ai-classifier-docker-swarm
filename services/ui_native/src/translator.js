
import translations from './translations.json';

const t = (key) =>{
    const lang = navigator.language.slice(0, 2);
    return {__html: translations[lang][key] || translations.en[key] || key };
}

export default t;
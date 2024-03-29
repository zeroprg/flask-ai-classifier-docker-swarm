const countries = [
    { cc: 'AF', name: 'Afghanistan' },
    { cc: 'AL', name: 'Albania' },
    { cc: 'AS', name: 'American Samoa' },
    { cc: 'AD', name: 'Andorra' },
    { cc: 'AO', name: 'Angola' },
    { cc: 'AI', name: 'Anguilla' },
    { cc: 'AQ', name: 'Antarctica' },
    { cc: 'AG', name: 'Antigua and Barbuda' },
    { cc: 'AR', name: 'Argentina' },
    // more countries...
    
    {cc: 'RU', name: 'Russia'},
    {cc: 'US', name: 'United States'},
    {cc: 'CA', name: 'Canada'},
    {cc: 'MX', name: 'Mexico'},
    {cc: 'GB', name: 'United Kingdom'},
    {cc: 'DE', name: 'Germany'},
    {cc: 'FR', name: 'France'},
    {cc: 'ES', name: 'Spain'},
    {cc: 'IT', name: 'Italy'},
    {cc: 'PT', name: 'Portugal'},
    {cc: 'NL', name: 'Netherlands'},
    {cc: 'BE', name: 'Belgium'},
    {cc: 'LU', name: 'Luxembourg'},
    {cc: 'CH', name: 'Switzerland'},
    {cc: 'AT', name: 'Austria'},
    {cc: 'CZ', name: 'Czech Republic'},
    {cc: 'PL', name: 'Poland'},
    {cc: 'HU', name: 'Hungary'},
    {cc: 'SK', name: 'Slovakia'},
    {cc: 'SE', name: 'Sweden'},
    {cc: 'NO', name: 'Norway'},
    {cc: 'FI', name: 'Finland'},
    {cc: 'DK', name: 'Denmark'},
    {cc: 'IE', name: 'Ireland'},
    {cc: 'AU', name: 'Australia'},
    {cc: 'NZ', name: 'New Zealand'},
    {cc: 'JP', name: 'Japan'},
    {cc: 'KR', name: 'South Korea'},
    {cc: 'CN', name: 'China'},
    {cc: 'IN', name: 'India'},
    {cc: 'SG', name: 'Singapore'},
    {cc: 'MY', name: 'Malaysia'},
    {cc: 'ID', name: 'Indonesia'},
    {cc: 'TH', name: 'Thailand'},
    {cc: 'VN', name: 'Vietnam'},
    {cc: 'PH', name: 'Philippines'},
    {cc: 'SA', name: 'Saudi Arabia'},
    {cc: 'AE', name: 'United Arab Emirates'},
    {cc: 'QA', name: 'Qatar'},
    {cc: 'KW', name: 'Kuwait'},
    {cc: 'TR', name: 'Turkey'},
    {cc: 'ZA', name: 'South Africa'},
    {cc: 'TN', name: 'Tunisia'},
    {cc: 'NG', name: 'Nigeria'},
    {cc: 'KE', name: 'Kenya'},
    {cc: 'TZ', name: 'Tanzania'},
    {cc: 'UG', name: 'Uganda'},
    {cc: 'GH', name: 'Ghana'},
    {cc: 'CI', name: 'Ivory Coast'},
    {cc: 'SN', name: 'Senegal'},
    {cc: 'CM', name: 'Cameroon'},
    {cc: 'MA', name: 'Morocco'},
    {cc: 'ET', name: 'Ethiopia'},
    {cc: 'SD', name: 'Sudan'},
    {cc: 'DZ', name: 'Algeria'},
    {cc: 'AM', name: 'Armenia'},
    {cc: 'EG', name: 'Egypt'},
    {cc: 'NI', name: 'Nicarugua'},
    {cc: 'LA', name: 'Laos'},
    {cc: 'IL', name: 'Israil'},
    {cc: 'HN', name: 'Honduras'},
    {cc: 'PS', name: 'Palestine'},
    {cc: 'PY', name: 'Paragway'},
    {cc: 'SY', name: 'Syria'},    
  {cc: 'LY', name: 'Libya'},
  {cc: 'MA', name: 'Morocco'},
  {cc: 'TN', name: 'Tunisia'},
  {cc: 'BJ', name: 'Benin'},
  {cc: 'BF', name: 'Burkina Faso'},
  {cc: 'CV', name: 'Cape Verde'},
  {cc: 'CI', name: "Cote d'Ivoire"},
  {cc: 'GM', name: 'Gambia'},
  {cc: 'GH', name: 'Ghana'},
  {cc: 'GN', name: 'Guinea'},
  {cc: 'GW', name: 'Guinea-Bissau'},
  {cc: 'LR', name: 'Liberia'},
  {cc: 'ML', name: 'Mali'},
  {cc: 'MR', name: 'Mauritania'},
  {cc: 'NE', name: 'Niger'},
  {cc: 'NG', name: 'Nigeria'},
  {cc: 'SH', name: 'Saint Helena'},
  {cc: 'SN', name: 'Senegal'},
  {cc: 'SL', name: 'Sierra Leone'},
  {cc: 'TG', name: 'Togo'},
  {cc: 'AO', name: 'Angola'},
  {cc: 'CD', name: 'Democratic Republic of the Congo'},
  {cc: 'CF', name: 'Central African Republic'},
  {cc: 'CG', name: 'Republic of the Congo'},
  {cc: 'CM', name: 'Cameroon'},
  {cc: 'GA', name: 'Gabon'},
  {cc: 'GQ', name: 'Equatorial Guinea'},
  {cc: 'ST', name: 'Sao Tome and Principe'},
  {cc: 'BW', name: 'Botswana'},
  {cc: 'LS', name: 'Lesotho'},
  {cc: 'MG', name: 'Madagascar'},
  {cc: 'MW', name: 'Malawi'},
  {cc: 'MU', name: 'Mauritius'},
  {cc: 'MZ', name: 'Mozambique'},
  {cc: 'RE', name: 'Reunion'},
  {cc: 'RW', name: 'Rwanda'},
  {cc: 'SC', name: 'Seychelles'},
  {cc: 'ZA', name: 'South Africa'},
  {cc: 'ZM', name: 'Zambia'},
  {cc: 'ZW', name: 'Zimbabwe'},
  {cc: 'SZ', name: 'Eswatini'},
  {cc: 'ER', name: 'Eritrea'},
  {cc: 'ET', name: 'Ethiopia'},
  {cc: 'KE', name: 'Kenya'},
  {cc: 'KM', name: 'Comoros'},
  {cc: 'MG', name: 'Madagascar'},
  {cc: 'MU', name: 'Mauritius'},
  {cc: 'MW', name: 'Malawi'},
  {cc: 'MZ', name: 'Mozambique'},
  {cc: 'RW', name: 'Rwanda'},
  {cc: 'SC', name: 'Seychelles'},
  {cc: 'SO', name: 'Somalia'},
  {cc: 'TZ', name: 'Tanzania'},
  {cc: 'UG', name: 'Uganda'},
  //more....
  { cc: 'MD', name: 'Moldova' },
  { cc: 'IR', name: 'Iran' },
  { cc: 'RO', name: 'Romania' },
  { cc: 'LT', name: 'Lithuania' },
  { cc: 'CL', name: 'Chile' },
  { cc: 'LV', name: 'Latvia' },
  { cc: 'TW', name: 'Taiwan' },
  { cc: 'BD', name: 'Bangladesh' },
  { cc: 'CO', name: 'Colombia' },
  { cc: 'GR', name: 'Greece' },
  { cc: 'RS', name: 'Serbia' },
  { cc: 'UA', name: 'Ukraine' },
  { cc: 'BG', name: 'Bulgaria' },
  { cc: 'PR', name: 'Puerto Rico' },
  { cc: 'BA', name: 'Bosnia and Herzegovina' },
  { cc: 'AD', name: 'Andorra' },
  { cc: 'TT', name: 'Trinidad and Tobago' },
  { cc: 'HK', name: 'Hong Kong' },
  { cc: 'CY', name: 'Cyprus' },
  { cc: 'null', name: 'Unknown' },
  { cc: 'CR', name: 'Costa Rica' },
  { cc: 'SI', name: 'Slovenia' },
  { cc: 'ME', name: 'Montenegro' },
  { cc: 'IM', name: 'Isle of Man' },
  { cc: 'KY', name: 'Cayman Islands' },
  { cc: 'MK', name: 'North Macedonia' },
  { cc: 'KH', name: 'Cambodia' },
  { cc: 'GG', name: 'Guernsey' },
  { cc: 'KZ', name: 'Kazahstan'},
  { cc: 'EE', name: 'Estonia'},
  { cc: 'BY', name: 'Belarussia'},
  { cc: 'BY', name: 'Belarussia'},
  { cc: 'BR', name: 'Brasil'},
  { cc: 'KR', name: 'South Korea'},
  { cc: 'CN', name: 'China'},
  { cc: 'GG', name: 'Guernsey'},
  { cc: 'RE', name: 'Réunion'},
  { cc: 'PR', name: 'Puerto Rico'},  
  { cc: 'KR', name: 'South Korea'},
  { cc: 'KY', name: 'Cayman Islands'},
  { cc: 'IM', name: 'Isle of Man'},  
  { cc: 'HK', name: 'Hong Kong SAR China'}
  ];
  
  export default countries;
  
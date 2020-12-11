// testing data 
export const fakeObjectOfInterest = [
    {hashcode: 'ABCF23422323' , currenttime: 1601476686.8732808, frame: 'data:image/jpeg;' }]

    
const timestamp = new Date('May 23 2017').getTime();
const ONE_DAY = 864000;

const DATA_SCATTER = [{label:'car',
    values: [
        {x: new Date(2015, 2, 5), y: 1},
        {x: new Date(2015, 2, 6), y: 2},
        {x: new Date(2015, 2, 7), y: 0},
        {x: new Date(2015, 2, 8), y: 3},
        {x: new Date(2015, 2, 9), y: 2},
        {x: new Date(2015, 2, 10), y: 3},
        {x: new Date(2015, 2, 11), y: 4},
        {x: new Date(2015, 2, 12), y: 4},
        {x: new Date(2015, 2, 13), y: 1},
        {x: new Date(2015, 2, 14), y: 5},
        {x: new Date(2015, 2, 15), y: 0},
        {x: new Date(2015, 2, 16), y: 1},
        {x: new Date(2015, 2, 16), y: 1},
        {x: new Date(2015, 2, 18), y: 4},
        {x: new Date(2015, 2, 19), y: 4},
        {x: new Date(2015, 2, 20), y: 5},
        {x: new Date(2015, 2, 21), y: 5},
        {x: new Date(2015, 2, 22), y: 5},
        {x: new Date(2015, 2, 23), y: 1},
        {x: new Date(2015, 2, 24), y: 0},
        {x: new Date(2015, 2, 25), y: 1},
        {x: new Date(2015, 2, 26), y: 1}
    ] },
    {label:'person',
    values: [
        {x: new Date(2015, 2, 5), y: 1},
        {x: new Date(2015, 2, 6), y: 2},
        {x: new Date(2015, 2, 7), y: 0},
        {x: new Date(2015, 2, 8), y: 3},
        {x: new Date(2015, 2, 9), y: 2},
        {x: new Date(2015, 2, 10), y: 3},
        {x: new Date(2015, 2, 11), y: 4},
        {x: new Date(2015, 2, 12), y: 4},
        {x: new Date(2015, 2, 13), y: 1},
        {x: new Date(2015, 2, 14), y: 5},
        {x: new Date(2015, 2, 15), y: 0},
        {x: new Date(2015, 2, 16), y: 1},
        {x: new Date(2015, 2, 16), y: 1},
        {x: new Date(2015, 2, 18), y: 4},
        {x: new Date(2015, 2, 19), y: 4},
        {x: new Date(2015, 2, 20), y: 5},
        {x: new Date(2015, 2, 21), y: 5},
        {x: new Date(2015, 2, 22), y: 5},
        {x: new Date(2015, 2, 23), y: 1},
        {x: new Date(2015, 2, 24), y: 0},
        {x: new Date(2015, 2, 25), y: 1},
        {x: new Date(2015, 2, 26), y: 1}
    ]
    }
    ]

const DATA1 = [
    {x0: ONE_DAY * 2, x: ONE_DAY * 3, y: 1},
    {x0: ONE_DAY * 7, x: ONE_DAY * 8, y: 1},
    {x0: ONE_DAY * 8, x: ONE_DAY * 9, y: 1},
    {x0: ONE_DAY * 9, x: ONE_DAY * 10, y: 2},
    {x0: ONE_DAY * 10, x: ONE_DAY * 11, y: 2.2},
    {x0: ONE_DAY * 19, x: ONE_DAY * 20, y: 1},
    {x0: ONE_DAY * 20, x: ONE_DAY * 21, y: 2.5},
    {x0: ONE_DAY * 21, x: ONE_DAY * 24, y: 1}
    ].map(el => ({x0: el.x0 + timestamp, x: el.x + timestamp, y: el.y}));
    
    const DATA2 = [
    {x0: ONE_DAY * 2, x: ONE_DAY * 3, y: 3},
    {x0: ONE_DAY * 7, x: ONE_DAY * 8, y: 4},
    {x0: ONE_DAY * 8, x: ONE_DAY * 9, y: 5},
    {x0: ONE_DAY * 9, x: ONE_DAY * 10, y: 1},
    {x0: ONE_DAY * 10, x: ONE_DAY * 11, y: 1.2},
    {x0: ONE_DAY * 19, x: ONE_DAY * 20, y: 1.7},
    {x0: ONE_DAY * 20, x: ONE_DAY * 21, y: 1.5},
    {x0: ONE_DAY * 21, x: ONE_DAY * 24, y: 5}
    ].map(el => ({x0: el.x0 + timestamp, x: el.x + timestamp, y: el.y}));
        

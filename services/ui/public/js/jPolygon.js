

var Polygon = function( complete, canvas, ctx){
 this.complete = complete;
 this.canvas = canvas;
 this.perimeter = new Array();
 this.ctx = ctx;
}


var dict = {};

//var perimeter = new Array();
//var complete = false;
//var canvas;
//var ctx;


   
 function refresh(cam) {
     var canvas_div =  document.getElementById("canvas_div"+cam);
     var right_div =  document.getElementById("right_div"+cam);
     var canvas = document.getElementById("jPolygon"+cam);
     var drwZone = document.getElementById("drwZone"+cam);
     if( ! dict[cam] ) {
       var ctx = canvas.getContext('2d');
       dict[cam] = new Polygon(false, canvas, ctx);
     }
     var img = document.getElementById('stream'+cam);
    // copy image dimensions
     var width =  img.width;
     var height =  img.height;
     dict[cam].canvas.width = width;
     dict[cam].canvas.height = height;
     
     if(  img.style.display == 'block' ) {
     	img.style.display = 'none';
        canvas_div.style.display = 'block';
    //    right_div.style.display = 'none';
        drwZone.innerHTML ="Show video";
        var imageObj = new Image();
        imageObj.onload = function() {
            dict[cam].ctx.drawImage(imageObj, 0, 0, canvas.width, canvas.height);  
            if(dict[cam].perimeter.length > 0 ) draw(true,cam);    
        };
        imageObj.src = canvas.getAttribute('data-imgsrc');
        dict[cam].ctx.drawImage(imageObj, 0, 0);
        
     } else {
     	img.style.display = 'block';
        canvas_div.style.display = 'none';
        drwZone.innerHTML ="Show zones";
   //     right_div.style.display = 'block';
     }
 };   

 function restart(with_draw,cam) {
    var img = new Image();
    img.src = dict[cam].canvas.getAttribute('data-imgsrc');

    img.onload = function(){
        dict[cam].ctx = dict[cam].canvas.getContext("2d");
        dict[cam].ctx.drawImage(img, 0, 0, dict[cam].canvas.width, dict[cam].canvas.height);
        if(with_draw == true){
            draw(false,cam);
        }
    }
};


function line_intersects(p0, p1, p2, p3) {
    var s1_x, s1_y, s2_x, s2_y;
    s1_x = p1['x'] - p0['x'];
    s1_y = p1['y'] - p0['y'];
    s2_x = p3['x'] - p2['x'];
    s2_y = p3['y'] - p2['y'];

    var s, t;
    s = (-s1_y * (p0['x'] - p2['x']) + s1_x * (p0['y'] - p2['y'])) / (-s2_x * s1_y + s1_x * s2_y);
    t = ( s2_x * (p0['y'] - p2['y']) - s2_y * (p0['x'] - p2['x'])) / (-s2_x * s1_y + s1_x * s2_y);

    if (s >= 0 && s <= 1 && t >= 0 && t <= 1)
    {
        // Collision detected
        return true;
    }
    return false; // No collision
}

function point(x, y,cam){
    dict[cam].ctx.fillStyle="white";
    dict[cam].ctx.strokeStyle = "white";
    dict[cam].ctx.fillRect(x-2,y-2,4,4);
    dict[cam].ctx.moveTo(x,y);
}

function undo(cam){
    dict[cam].ctx = undefined;
    dict[cam].perimeter.pop();
    dict[cam].complete = false;
    restart(true,cam);
}

function clear_canvas(cam){
    dict[cam].ctx = undefined;
    dict[cam].perimeter = new Array();
    dict[cam].complete = false;
    document.getElementById('coordinates' + cam).value = '';
    restart(false,cam);
}

function draw(end, cam){
    dict[cam].ctx.lineWidth = 1;
    dict[cam].ctx.strokeStyle = "white";
    dict[cam].ctx.lineCap = "square";
    dict[cam].ctx.beginPath();

    for(var i=0; i<dict[cam].perimeter.length; i++){
        if(i==0){
            dict[cam].ctx.moveTo(dict[cam].perimeter[i]['x'],dict[cam].perimeter[i]['y']);
            end || point(dict[cam].perimeter[i]['x'],dict[cam].perimeter[i]['y'], cam);
        } else {
            dict[cam].ctx.lineTo(dict[cam].perimeter[i]['x'],dict[cam].perimeter[i]['y']);
            end || point(dict[cam].perimeter[i]['x'],dict[cam].perimeter[i]['y'],cam);
        }
    }
    if(end){
        dict[cam].ctx.lineTo(dict[cam].perimeter[0]['x'],dict[cam].perimeter[0]['y']);
        dict[cam].ctx.closePath();
        dict[cam].ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
        dict[cam].ctx.fill();
        dict[cam].ctx.strokeStyle = 'blue';
        dict[cam].complete = true;
    }
    dict[cam].ctx.stroke();

    // print coordinates
    if(dict[cam].perimeter.length == 0){
        document.getElementById('coordinates'+cam).value = '';
    } else {
        document.getElementById('coordinates'+cam).value = JSON.stringify(dict[cam].perimeter);
    }
}




function check_intersect(x,y,cam){
    if(dict[cam].perimeter.length < 4){
        return false;
    }
    var p0 = new Array();
    var p1 = new Array();
    var p2 = new Array();
    var p3 = new Array();
    var l = dict[cam].perimeter.length-1;
    p2['x'] = dict[cam].perimeter[l]['x'];
    p2['y'] = dict[cam].perimeter[l]['y'];
    p3['x'] = x;
    p3['y'] = y;

    for(var i=0; i<l; i++){
        p0['x'] = dict[cam].perimeter[i]['x'];
        p0['y'] = dict[cam].perimeter[i]['y'];
        p1['x'] = dict[cam].perimeter[i+1]['x'];
        p1['y'] = dict[cam].perimeter[i+1]['y'];
        if(p1['x'] == p2['x'] && p1['y'] == p2['y']){ continue; }
        if(p0['x'] == p3['x'] && p0['y'] == p3['y']){ continue; }
        if(line_intersects(p0,p1,p2,p3)==true){
            return true;
        }
    }
    return false;
}



function point_it(event,cam) {
    if(dict[cam].complete){
        alert('Polygon already created');
        return false;
    }
    var rect, x, y;

   if(event.ctrlKey || event.which === 3 || event.button === 2 ||  
              event.target.innerText == "Close Polygon" ) {
 
        if(dict[cam].perimeter.length==2){
            alert('You need at least three points for a polygon');
            return false;
        }
        x = dict[cam].perimeter[0]['x'];
        y = dict[cam].perimeter[0]['y'];
        if(check_intersect(x,y,cam)){
            alert('The line you are drowing intersect another line');
            return false;
        }
        draw(true,cam);
        //alert('Polygon closed');
	event.preventDefault();
        return false;
    } else {
        rect = dict[cam].canvas.getBoundingClientRect();
        x = event.clientX - rect.left;
        y = event.clientY - rect.top;
        var l = dict[cam].perimeter.length;
        if (l>0 && x == dict[cam].perimeter[l-1]['x'] && y == dict[cam].perimeter[l-1]['y']){
            // same point - double click
            return false;
        }
        if(check_intersect(x,y,cam)){
            alert('The line you are drowing intersect another line');
            return false;
        }
        dict[cam].perimeter.push({'x':x,'y':y});
        draw(false,cam);
        return false;
    }
}


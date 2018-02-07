//Capture geometry of the feature in your map 
var feature = Geometry($feature);

//Add map coordinates for the incident 
var incident = {"x":-13522551.111,"y":4660872.00986, 
                "spatialReference": {"latestWkid": 3857, "wkid": 102100}};

//Buffer the incident
var buff = buffer(Point(incident), 2.0, "miles");

//Return the rendering based on the intersect 
IF (Intersects(feature,buff)) {
    
    return "Feature within 2 miles of the Incident"
    
} else {
    
    return "Feature more than 2 miles from the Incident"
}


//other helpful link: https://gist.github.com/keum/7441007
//Tranform coords from 4326 to 3857 (or 102100): https://mygeodata.cloud/cs2cs/
/*
Name:       buffer_example.js

Created:    2/9/18

Purpose:    Buffers point "incident" and intersects all map features within a
            user specified distance from the point.

Helpful Links:
https://mygeodata.cloud/cs2cs/
https://developers.arcgis.com/javascript/3/jshelp/arcade.html
*/

//Capture geometry of the feature in your map
var feature = Geometry($feature);

//Add map coordinates for the incident
var incident = {"x":-13522551.111,"y":4660872.00986,
                "spatialReference": {"latestWkid": 3857, "wkid": 102100}};

//Buffer the incident
var dist = 1000;
var units = "meters";
var buff = buffer(Point(incident), dist, units);

//Return the rendering based on the intersect
IF (Intersects(feature,buff)) {

    return "Feature within " + dist + " " + units + " of the Incident"

} else {

    return "Feature more than " + dist + " " + units + " from the Incident"
}

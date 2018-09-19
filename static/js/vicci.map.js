var vicciMapStyle = [
  {
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e3d7ce"
      }
    ]
  },
  {
    "elementType": "labels.icon",
    "stylers": [
      {
        "visibility": "off"
      }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#616161"
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#f5f5f5"
      }
    ]
  },
  {
    "featureType": "administrative.land_parcel",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#bdbdbd"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#cbb6a7"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#757575"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#c2d0b9"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#ffffff"
      }
    ]
  },
  {
    "featureType": "road.arterial",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#757575"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#f6c653"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#616161"
      }
    ]
  },
  {
    "featureType": "road.local",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  },
  {
    "featureType": "transit.line",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#866053"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#c9c9c9"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9e9e9e"
      }
    ]
  }
];


var infoWindow_base = $('.infowindow_base');
var prev_infowindow = false;
var markers = [];
var waypoints = [];

function createMarker(map, latlng, info, visible, is_waypoint, marker_callback){
    var windowContent = infoWindow_base.clone()
        .find('.title').text(info['title']).end()
        .find('.address').text(info['address']==null?'':info['address']).end()
        .find('img').attr('src', info['img']).end();

    var infowindow = new google.maps.InfoWindow({
        content: windowContent.html(),
        maxWidth: 350
    });

    var marker = new RichMarker({
          position: latlng,
          map: map,
          infowindow: infowindow,
          content: '<div class="marker-wrapper"><div class="marker"><img src="' + info['img'] + '"></div></div>'
    });
    marker['pk'] = info['pk'];
    marker.visible = visible;
    markers.push(marker);

    if (is_waypoint){
        waypoints.push({ 'location': latlng, 'stopover':true} );
    }

    google.maps.event.addListener(marker, 'click', (function(marker, infowindow){
        return function() {
            if( prev_infowindow ) {
               prev_infowindow.close();
            }
            prev_infowindow = infowindow;
            this.infowindow.open(map, this);

             console.log(marker_callback);

            if ((marker_callback) && ( typeof marker_callback == 'function')){
                marker_callback(marker);
            }
        };
    })(marker, infowindow));

    return marker;
}

function setActive(map, marker, active){
    var pin = $(marker.getContent()).toggleClass('active', active);
    marker.setContent(pin[0]);
}

function hideMarker(map, marker){
    marker.setVisible(false);
    if (marker.infowindow){
        marker.infowindow.close(map, marker);
    }
}

function fitBoundsToMarkers(map, only_visible){

    var bounds = new google.maps.LatLngBounds();
    var visibleCount = 0;
    for (marker of markers){
        if (!only_visible || marker.visible){
            visibleCount++;
            bounds.extend(marker.position);
        }
    }

    if (visibleCount > 0){
        map.fitBounds(bounds, 50);

    }
}

function centerMap(map, marker){
    map.panTo(marker.position);
    map.setZoom(15);
}
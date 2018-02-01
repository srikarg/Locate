var socket;

$(function() {
    var room_members = $('.room-members');
    var map = null;
    var userCenter = [];
    var markers = [];

    $(window).on('unload', function() {
        socket.emit('left', {});
    });

    socket = io();

    socket.on('connect', function() {
        socket.emit('joined', {});
    });

    socket.on('list of users', function(data) {
        room_members.empty();
        for (var i = 0; i < data.users.length; i++) {
            room_members.append('<li>' + data.users[i] + '</li>');
        }
    });

    socket.on('update locations', function(data) {
        deleteAllMarkers();
        for (var user in data.userData) {
            addMarker(user, data.userData[user].lat, data.userData[user].lng);
        }
    });

    var getUserLocation = function(callback) {
        if (window.navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                callback(position);
            }, function(error) {
                console.log(error);
            }, {
                enableHighAccuracy: true,
                timeout: 10000
            });
        }
    };

    var deleteAllMarkers = function() {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
        }
        markers.length = 0;
        markers = [];
    };

    var addMarker = function(username, lat, lng) {
        var marker = new google.maps.Marker({
            map: map,
            position: new google.maps.LatLng(lat, lng),
            title: username + ' is here!'
        });

        markers.push(marker);

        infoWindow = new google.maps.InfoWindow();

        google.maps.event.addListener(marker, 'click', (function(marker) {
            return function() {
                infoWindow.setContent('<div class="info-window"><p>' + marker.title + '</p></div>');
                infoWindow.open(map, marker);
            };
        })(marker));
    };

    var initialize = function() {
        var mapOptions = null;

        getUserLocation(function(position) {
            userCenter[0] = position.coords.latitude;
            userCenter[1] = position.coords.longitude;

            if (userCenter.length !== 0) {
                mapOptions = {
                    center: new google.maps.LatLng(userCenter[0], userCenter[1]),
                    zoom: 16
                };
            }

            map = new google.maps.Map(document.getElementById('map'), mapOptions);

            socket.emit('new location', { position: userCenter });
        });
    };

    initialize();
});

function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        window.location.href = '/';
    });
}

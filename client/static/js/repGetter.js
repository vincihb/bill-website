"use strict";
var reps;

function getYourReps(address) {
    if (getCookieProperty('address'))
        getReps(JSON.parse(getCookieProperty('address')));
    else {
        if (address)
            getReps(address);
        else
            getIP(getReps);
    }
}

function getIP(callback) {
    $.get('https://ipapi.co/json/', function(data) {
        callback({string: data.postal});
    });
}

function getReps(address) {
    var url = 'https://www.googleapis.com/civicinfo/v2/representatives?address=' + address.string +
        '&levels=country&roles=legislatorLowerBody&roles=legislatorUpperBody&alt=json&key=AIzaSyCo65iidbpfiBeKTBiKIbkQOopq5ldMG-o';
    $.get(url, function(repResult) {
        appendRepInfoToPage(repResult, address);
    });
}

function appendRepInfoToPage(repInfo, address) {
    var trg = $('#repTarget');
    trg[0].innerHTML = '<div id="senate">\n' +
        '                    <h4>Your Senators:</h4><br>\n' +
        '                </div>\n' +
        '                <div id="house">\n' +
        '                    <h4>Your Member of Congress:</h4><br>\n' +
        '                </div>';
    reps = repInfo;
    var tempTrg;
    var senate = $('#senate');
    var house = $('#house');
    var official;

    if (address.city)
        trg.prepend("<h3>Your representatives in " + address.city + ", " + address.state + " are:</h3>");
    else
        trg.prepend("<h3>Based on your IP, your representatives in " + repInfo.normalizedInput.city + ", " +
            repInfo.normalizedInput.state + " are:</h3>");

    for (var i in repInfo.offices) {
        if (repInfo.offices[i].name === "United States Senate")
            tempTrg = senate;
        else
            tempTrg = house;

        for (var j in repInfo.offices[i].officialIndices) {
            official = repInfo.officials[repInfo.offices[i].officialIndices[j]];
            if (official.photoUrl)
                tempTrg.append(getMemberChunkToAdd(official));
            else
                getMissingImgAndAppend(official, tempTrg);
        }
    }

    if (repInfo.offices.length < 2)
        trg.append('<p>It looks like your ZIP code is part of multiple congressional districts! If you ' +
            '<button data-toggle="modal" data-target="#addressModal">provide your address</button>' +
            ' we can provide more information on your congressional representatives</p>');
    else {
        trg.append('<p>Still not right? <button data-toggle="modal" data-target="#addressModal">Update your address!' +
            '</button></p>');

        if (getCookieProperty('address')) {
            trg.append('<i>Your saved address is: ' + JSON.parse(getCookieProperty('address')).string + '</i>');
        }
    }

}

function getMemberChunkToAdd(official) {
    var badge = 'success';
    if (official.party === 'Republican')
        badge = 'danger';
    else if (official.party === 'Democratic')
        badge = 'primary';

    return '<div class="row">\
                <div class="col-sm-3">\
                    <a href="' + official.photoUrl + '">\
                       <img src="' + official.photoUrl + '" alt="Photo of ' + official.name+ '" class="rep-img">\
                    </a>\
                </div>\
                <div class="col-sm-9">\
                    <h5>' + official.name + '\
                        <span style="display: inline-block" class="badge badge-' + badge + '">' + official.party + '</span>\
                    </h5>\
                    <h5>Phone Number: <a href="tel:1-' + official.phones + '">1 ' + official.phones + '</h5>\
                    <button>Call Them!</button> <button>Email Them!</button>\
                </div>\
            </div>\
            <hr>';
}

function getMissingImgAndAppend(official, trg) {
    var temp = official.name.split(' ');
    var firstName, lastName;
    firstName = temp[0];
    lastName = temp[temp.length-1];

    var content = {first: firstName, last: lastName};

    $.post({
        url: '/missing',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(content)
    }, function(data) {
        if (data) {
            data = JSON.parse(data);
            official.photoUrl = data.photoUrl;
            trg.append(getMemberChunkToAdd(official));
        }
        else {
            console.log('invalid request');
            trg.append(getMemberChunkToAdd(official));
        }
    })
}

function newSearch() {
    var addr = getModalAddress();
    if ($('#saveAddr')[0].checked)
        document.cookie = "address=" + JSON.stringify(addr);

    getReps(addr);
}

function getModalAddress() {
    var line1 = $('#line-1').val();
    var city = $('#city').val();
    var state = $('#state').val();
    var zip = $('#zip').val();

    line1 = line1 ? line1 : '';
    city = city ? city : '';
    state = state ? state : '';
    zip = zip ? zip.slice(0, 5) : '';
    if (line1 && city && state && zip)
        return {
            street: line1,
            city: city,
            state: state,
            zip: zip,
            string: line1 + ' ' + city + ' ' + state + ', ' + zip
        };
    else if (line1 && city && state && !zip)
        return {
            street: line1,
            city: city,
            state: state,
            string: line1 + ' ' + city + ' ' + state
        };
    else
        return {
            zip: zip,
            string: zip
        }
}

/**
 * Thanks to kirlich from https://stackoverflow.com/questions/10730362/get-cookie-by-name
 * @param name
 * @return {*}
 */
function getCookieProperty(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2)
        return parts.pop().split(";").shift();
}
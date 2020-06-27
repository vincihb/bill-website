'use strict';

// pages like: 'https://en.wikipedia.org/wiki/115th_United_States_Congress'
function getNextPage(currentSession) {
    if (typeof currentSession !== 'number')
        currentSession = Number(currentSession);

    // cast session to string
    const nextSession = currentSession + 1;
    let session = '' + nextSession;

    // add one to reflect our new
    const hundredsModulo = (nextSession % 100);
    const tensModulo = (nextSession % 10);

    // anything between 10 and 20 ends with "th"
    if (hundredsModulo > 10 && hundredsModulo < 20)
        session += 'th';
    else if (tensModulo === 1)
        session += 'st';
    else if (tensModulo === 2)
        session += 'nd';
    else if (tensModulo === 3)
        session += 'rd';
    else
        session += 'th';

    return `https://en.wikipedia.org/wiki/${session}_United_States_Congress`;
}
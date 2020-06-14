'use strict';

/**
 * Scrape all of the members of congress, metadata and links from the wikipedia pages
 */

window.lastTry = null;

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

function scrape() {
    let session = window.location.href.replace('https://en.wikipedia.org/wiki/', '').slice(0, 3);
    if (isNaN(Number(session[2])))
        session = session.slice(0, 2);

    if (isNaN(Number(session[1])))
        session = session.slice(0, 1);

    const data = {
        session: Number(session),
        senate: [],
        house: []
    };

    // get the first date from the infobox on this page.. this tends to be the start and end dates for a sesison
    const dates = document.querySelector('.infobox').innerText
        .split('\n').filter(el => el.match(/\s\d{4}\s\W\s\w{2}/g))[0];

    const startDate = dates.split('–')[0].trim();
    const endDate = dates.split('–')[1].trim();

    const anchorNode = document.querySelector('#Members').parentNode;
    let result = resolveSectionTable(anchorNode);
    const senateDiv = result.lastDiv;
    const senateTable = result.table;

    const senateTd1 = senateTable.querySelectorAll('td')[0];
    const senateTd2 = senateTable.querySelectorAll('td')[1];
    extractDataFromTD(senateTd1, false);
    extractDataFromTD(senateTd2, false);

    result = resolveSectionTable(senateDiv);
    const houseTable = result.table;

    const houseTd1 = houseTable.querySelectorAll('td')[0];
    const houseTd2 = houseTable.querySelectorAll('td')[1];
    extractDataFromTD(houseTd1, true);
    extractDataFromTD(houseTd2, true);

    console.log(data);
    window.lastTry = data;

    download('Congress - ' + session + '.json', JSON.stringify(data));
    window.location.href = getNextPage(session);

    function resolveSectionTable(anchor) {
        let nextDiv = next(anchor, 'div');
        let divTable = nextDiv.querySelector('table');

        while (!divTable) {
            nextDiv = next(nextDiv, 'div');
            divTable = nextDiv.querySelector('table');
        }

        return {table: divTable, lastDiv: nextDiv};
    }

    function extractDataFromTD(td, isHouse) {
        let current = td.querySelector('h4');
        while (current) {
            let state = current.innerText.replace('[edit]', '').trim();
            let senators = Array.from(next(current, 'ul').children);
            senators.forEach((child) => {
                // if the child has a nested list
                if (child.querySelector('ul'))
                    appendTiered(state, child, isHouse);
                else
                    appendNonTiered(state, child, isHouse);
            });

            current = next(current, 'h4')
        }
    }

    function appendTiered(state, child, isHouse) {
        // capture the replacements
        const replacements = child.querySelectorAll('li');

        // clone the node and splice out the ul
        const clone = child.cloneNode(true);
        clone.removeChild(clone.querySelector('ul'));

        // we can now extract the needed data from the clone
        let extracted = extractData(state, clone, isHouse);

        // we do need to retain the district number for the replacements
        const district = extracted.district;
        Array.from(replacements).forEach(replacement => {
            extractData(state, replacement, isHouse, district)
        });
    }

    function extractData(state, child, isHouse, districtNumber) {
        let link = Array.from(child.children).filter((el) => el.tagName === 'A')[0];
        let href = link ? link.getAttribute('href') : null;
        if (href && href.indexOf('https') === -1)
            href = 'https://en.wikipedia.org' + href;

        const inner = child.innerText;

        let name;
        if (link)
            name = link.innerText;
        else
            name = inner.split('.').slice(1).join('.').split('(')[0].split(',')[0].trim();

        let party = 'O';
        if (inner.split('(').length > 1)
            party = inner.split('(')[1].split(')')[0];

        const district = districtNumber || inner.split('.')[0];

        let overrideStartYear;
        if (inner.includes(', from'))
            overrideStartYear = inner.split(', from')[1].trim();

        let overrideEndYear;
        if (inner.includes(', until'))
            overrideEndYear = inner.split(', until')[1].trim();

        if (inner.includes(' – ') && inner.includes('), ')) {
            let dates = inner.split('), ')[1].trim();
            dates = dates.split(' – ');
            overrideStartYear = dates[0].trim();
            overrideEndYear = dates[1].trim();
        }

        let collectedData = {
            state,
            name,
            party: getPartyNameMap()[party],
            partyAbbreviation: party,
            district,
            startDate: overrideStartYear || startDate,
            endDate: overrideEndYear || endDate,
            href
        };

        if (isHouse)
             data.house.push(collectedData);
        else
            data.senate.push(collectedData);

        return collectedData;
    }

    function appendNonTiered(state, child, isHouse) {
        extractData(state, child, isHouse);
    }

    function next(startElement, selector) {
        const maxSearchDepth = 50;
        let searchDepth = 0;
        let element = startElement.nextSibling;
        while (element) {
            if (element.tagName && element.tagName.toLowerCase() === selector.toLowerCase())
                return element;

            element = element.nextSibling;

            if (++searchDepth > maxSearchDepth)
                return null;
        }

        return element;
    }

    function getPartyNameMap() {
        const session = data.session;
        if (session <= 32)
            return scrape.PARTY_MAP_BEFORE_32;
        else if (session < 42)
            return scrape.PARTY_MAP_AFTER_32;
        else if (session < 60)
            return scrape.PARTY_MAP_AFTER_42;
        else if (session < 64)
            return scrape.PARTY_MAP_AFTER_60;
        else if (session < 73)
            return scrape.PARTY_MAP_AFTER_64;
        else
            return scrape.PARTY_MAP_AFTER_73;
    }

    function download(filename, text) {
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();
        document.body.removeChild(element);
    }
}


// copy and add party identifiers as needed
// some identifiers change over time... so need to be reassigned as we progress through wikipedia
scrape.CORE_PARTIES = {
    'D': 'Democratic',
    'R': 'Republican',
    'I': 'Independent',
    'O': 'Other',
};

scrape.PARTY_MAP_BEFORE_32 = {
    ...scrape.CORE_PARTIES,
    'P': 'Pro-Administration',
    'A': 'Anti-Administration',
    'J': 'Jacksonian',
    'Anti-J': 'Anti-Jacksonian',
    'DR': 'Democratic-Republican',
    'F': 'Federalist',
    'AJ': 'Anti-Jacksonian',
    'N': 'Nullifier',
    'SR': 'States\' Rights',
    'AM': 'Anti-Masonic',
    'W': 'Whig',
    'ID': 'Independent Democratic',
    'LO': 'Law and Order',
    'IW': 'Independent Whig',
    'C': 'Conservative',
    'FS': 'Free Soil',
    'U': 'Unionist'
};

scrape.PARTY_MAP_AFTER_32 = {
    ...scrape.PARTY_MAP_BEFORE_32,
    'A': 'American (Know Nothing)',
    'UU': 'Unconditional Unionist',
    'Conservative': 'Conservative'
};

scrape.PARTY_MAP_AFTER_42 = {
    ...scrape.PARTY_MAP_AFTER_32,
    'UU': 'Unconditional Unionist',
    'LR': 'Liberal Republican',
    'AM': 'Anti-Monopoly',
    'G': 'Greenback',
    'GB': 'Greenback',
    'RA': 'Readjuster',
    'P': 'Populist',
    'S': 'Silver',
    'SR': 'Silver Republican'
};

scrape.PARTY_MAP_AFTER_60 = {
    ...scrape.PARTY_MAP_AFTER_42,
    'FL': 'Farmer Labor'
};

scrape.PARTY_MAP_AFTER_64 = {
    ...scrape.PARTY_MAP_AFTER_60,
    'P': 'Prohibition',
    'S': 'Socialist'
};

scrape.PARTY_MAP_AFTER_73 = {
    ...scrape.PARTY_MAP_AFTER_64,
    'P': 'Wisconsin Progressive',
    'AL': 'American Labor',
};

scrape();
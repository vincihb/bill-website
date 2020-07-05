'use strict';

class CITMemberList extends ManagedTable {
    constructor() {
        super(CITMemberList.headers, '');
    }

    apiRequest(successCallback, errorCallback) {
        request('/api/members', {}, successCallback, errorCallback, request.METHODS.GET);
    }

    getRow(dataRow, htmlRow) {
        let td = new ElementFactory(elements.TD);
        let linkElem = new ElementFactory(elements.A, '', './member/' + dataRow.id, dataRow.first_name + ' '  + dataRow.last_name);
        td.appendChild(linkElem);
        htmlRow.append(td);

        td = new ElementFactory(elements.TD, '', dataRow.party);
        htmlRow.append(td);

        td = new ElementFactory(elements.TD);
        if (dataRow.state)
            td.appendChild(new IconLinkElement('/assets/state/' + window.STATE_MAP[dataRow.state.toLowerCase()], dataRow.state, dataRow.state));

        htmlRow.appendChild(td);
    }

    getRowCorpusTerms(row, tags) {
        return (row.first_name + ' ' + row.last_name + ' ' + row.party + ' ' + row.state).toLowerCase();
    }
}

CITMemberList.headers = [
    {text: 'Name', isOrderable: true, parameterMapping: 'first_name'},
    {text: 'Party', isOrderable: true, parameterMapping: 'party'},
    {text: 'State', isOrderable: true, parameterMapping: 'state'}
];

defineCustomElement('cit-member-list', CITMemberList);
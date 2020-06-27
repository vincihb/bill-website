'use strict';


class CITMember extends _BaseDOM {
    constructor() {
        super();

        this.bootstrapStyles(true);
        this.getData();
    }

    getData() {
        const id = window.location.href.split('/').pop();
        request('/api/member/' + id, {}, response => {
            this.render(response.data);
        }, err => {
            console.error('Error processing request!');
            console.error(err);
        }, request.METHODS.GET)
    }

    render(data) {
        console.log(data);
        this.appendChild(new ElementFactory(elements.H2, '', data.first_name + ' ' + data.last_name));
        this.appendChild(new ElementFactory(elements.HR));
        this.appendChild(new ElementFactory(elements.P, '', 'data here!'));
    }
}

defineCustomElement('cit-member', CITMember);
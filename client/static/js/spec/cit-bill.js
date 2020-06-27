'use strict';


class CITBill extends _BaseDOM {
    constructor() {
        super();

        this.bootstrapStyles(true);
        this.getData();
    }

    getData() {
        const id = window.location.href.split('/').pop();
        request('/api/bill/' + id, {}, response => {
            this.render(response.data);
        }, err => {
            console.error('Error processing request!');
            console.error(err);
        }, request.METHODS.GET)
    }

    render(data) {
        this.appendChild(new ElementFactory(elements.H2, '', 'Bill - HR.204'));
        this.appendChild(new ElementFactory(elements.HR));
        // this.appendChild(new ElementFactory(elements.P, '', AboutPage.CONTENT[0]));
        // this.appendChild(new ElementFactory(elements.P, '', AboutPage.CONTENT[1]));
        this.appendChild(new ElementFactory(elements.P, '', 'data here!'));s
    }
}

defineCustomElement('cit-bill', CITBill);
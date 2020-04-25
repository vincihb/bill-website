'use strict';


class IndexPage extends _BaseDOM {
    constructor() {
        super();

        this.bootstrapStyles(true);
        this.addStyle('/alb-css/input/form.css');
        this.addStyle('/alb-css/input/input.css');

        this.appendChild(new ElementFactory(elements.H1, '', 'Where\'s That Bill?'));
        this.appendChild(new ElementFactory(elements.SPAN, '', 'The site for confused people who just want to know who to yell at about that one bill you should be outraged about.'))

        this.appendChild(new ElementFactory(elements.BR));
        this.appendChild(new ElementFactory(elements.BR));

        this.getSearchDiv();

        this.getRepGetter();
    }

    /**
     * TODO: Component-ify this
     */
    getSearchDiv() {
        this._searchDiv = new ElementFactory(elements.DIV);
        this._searchDiv.setAttribute(ATTRS.ID, 'search-div');
        this._searchDiv.appendChild(new ALBInput('text', 'Enter the name of a bill:', 'search',
            'i.e. Tax Bill, Obamacare...', {}));

        this._searchDiv.appendChild(new ElementFactory(elements.H5, '', 'OR'));
        this._searchDiv.appendChild(new ElementFactory(elements.H6, '', 'Select a Bill Being Talked About in The News'));

        const buttonGroup = new ElementFactory(elements.DIV, 'btn-group');
        const button1 = new ElementFactory(elements.BUTTON, 'btn btn-secondary active', 'Recent');
        const button2 = new ElementFactory(elements.BUTTON, 'btn btn-secondary', 'Popular');

        buttonGroup.appendChild(button1);
        buttonGroup.appendChild(button2);
        this._searchDiv.appendChild(buttonGroup);

        this._searchDiv.appendChild(new ElementFactory(elements.BR));
        this._searchDiv.appendChild(new ElementFactory(elements.BR));

        const popularBills = new ElementFactory(elements.DIV, 'popular-bills');
        popularBills.appendChild(new ElementFactory(elements.BUTTON, 'btn btn-sm btn-primary', 'Bill 1'));
        popularBills.appendChild(new ElementFactory(elements.BUTTON, 'btn btn-sm btn-primary', 'Bill 2'));
        popularBills.appendChild(new ElementFactory(elements.BUTTON, 'btn btn-sm btn-primary', 'Bill 3'));
        popularBills.appendChild(new ElementFactory(elements.BUTTON, 'btn btn-sm btn-primary', 'Bill 4'));
        popularBills.appendChild(new ElementFactory(elements.BUTTON, 'btn btn-sm btn-primary', 'Bill 5'));
        this._searchDiv.appendChild(popularBills);

        this.appendChild(this._searchDiv);
    }

    /**
     * TODO: Component-ify this
     */
    getRepGetter() {
        this._repDiv = new ElementFactory(elements.DIV, 'rep-div');
        this._repDiv.appendChild(new ElementFactory(elements.BR));
        this._repDiv.appendChild(new ElementFactory(elements.BUTTON, 'btn btn-primary', 'GET ME REPS'));
        this.appendChild(this._repDiv);
    }
}

customElements.define('index-page', IndexPage);
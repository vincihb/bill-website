'use strict';


class AboutPage extends _BaseDOM {
    constructor() {
        super();

        this.bootstrapStyles(true);

        this.appendChild(new ElementFactory(elements.H1, '', 'About'));
        this.appendChild(new ElementFactory(elements.HR));
        this.appendChild(new ElementFactory(elements.P, '', AboutPage.CONTENT[0]));
        this.appendChild(new ElementFactory(elements.P, '', AboutPage.CONTENT[1]));
    }
}

AboutPage.CONTENT = [
    'Where\'s That Bill? was initially written as a solo project by Michael Albinson in the winter of his senior year at Queen\'s University. ' +
    'He began his work in earnest after discovering that while abundant sources of data existed on legislative happenings, ' +
    'but none of it was structured in such a way as to ease the use and understanding of this data. ' +
    'The resulting data was to be made publicly available, easily searchable and quickly understandable.',

    'As work continued on the project it became apparent through conversations with potential users and members of ' +
    'congress that this site had the potential to aggregate large amounts of information to vastly simplify the number of ' +
    'locations a user had to search in order to find information about the current political goings-on, as well as the ' +
    'future of politics in an individual\'s district.'
];

defineCustomElement('about-page', AboutPage);
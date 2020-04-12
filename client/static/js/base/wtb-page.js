'use strict';


class WTBPage extends AppPage {
    render() {
        const footerAddendum = '<div>Where\'s That Bill? is written in Python and is open source. <a href="" target="_blank">See the GitHub repo.</a></div>' +
            '<div>Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>';


        this.header.setHeaderLinks([]);
        this.header.setHeroImage('/assets/logo.png', 'Where\'s that bill logo', 'header-img', 'header-img-wrap');
        this.header.render();

        this.footer.setCopyright('Website by Michael Albinson © 2017-2020');
        this.footer.setMetaLinks([{title: 'About', link: '/about'}]);
        this.footer.setHTMLAddendum(footerAddendum);
        this.footer.render();
    }
}

customElements.define('wtb-page', WTBPage);
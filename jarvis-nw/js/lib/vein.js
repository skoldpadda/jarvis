/**
 * vein.js - version 0.2
 * by Danny Povolotski (dannypovolotski@gmail.com)
 * Slight modifications by William Gaul
 */
!function(name, definition) {
    if (typeof module != 'undefined') {
        module.exports = definition();
    } else if (typeof define == 'function' && define.amd) {
        define(name, definition);
    } else {
        this[name] = definition();
    }
}('vein', function() {
    var vein = function() {};

    vein.prototype.setDocument = function(doc) {
        var self = this;
        self.doc = doc;
        return self;
    }

    // Get the stylesheet we use to inject stuff or create it if it doesn't exist yet
    vein.prototype.getStylesheet = function() {
        var self = this;
        if (!self.element) {
            self.element = self.doc.createElement("style");
            self.element.setAttribute('type', 'text/css');
            self.element.setAttribute('id', 'vein');
            self.doc.getElementsByTagName("head")[0].appendChild(self.element);

            // @TODO: Find a more reliable way to pair the element and the stylesheet object?
            self.stylesheet = self.doc.styleSheets[self.doc.styleSheets.length - 1];
            self.rules = self.stylesheet[self.doc.all ? 'rules' : 'cssRules'];
        }
        return self.element;
    };

    vein.prototype.inject = function(selectors, css) {
        var self = this, element = self.getStylesheet(), si, sl, matches, ri, rl, cssText, property, mi, ml;
        if (typeof selectors === 'string') {
            selectors = [selectors];
        }
        for (si = 0, sl = selectors.length; si < sl; si++) {
            matches = [];
            // Since there could theoretically be multiple versions of the same rule, we will first iterate
            for (ri = 0, rl = self.rules.length; ri < rl; ri++) {
                if (self.rules[ri].selectorText === selectors[si]) {
                    if (css === null) {
                        self.stylesheet.deleteRule(ri);
                    } else {
                        matches.push(self.rules[ri]);
                    }
                }
            }
            if (css === null) {
                return;
            }
            // Create ruleset for the selector if it does not exist, else modify
            if (matches.length === 0) {
                cssText = [];
                for (property in css) {
                    if (css.hasOwnProperty(property)) {
                        cssText.push(property + ': ' + css[property] + ';');
                    }
                }
                cssText = selectors[si] + '{' + cssText.join('') + '}';
                self.stylesheet.insertRule(cssText, self.rules.length);
            } else {
                for (mi = 0, ml = matches.length; mi < ml; mi++) {
                    for (property in css) {
                        if (css.hasOwnProperty(property)) {
                            // @TODO: Implement priority
                            matches[mi].style.setProperty(property, css[property], '');
                        }
                    }
                }
            }
        }
        return self;
    };

    return new vein();
});
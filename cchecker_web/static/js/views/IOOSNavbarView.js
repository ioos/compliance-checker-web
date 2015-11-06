/*
 * cchecker_web/static/js/views/IOOSNavbarView.js
 * Navbar with the IOOS theme
 */

var IOOSNavbarView = BaseView.extend({
  initialize:function(options) {
    options = _.extend({
      links: []
    }, options);

    this.links = options.links;

    BaseView.prototype.initialize.call(this);
  },
  templateName: "IOOSNavbar",
  render: function() {
    var self = this;
    this.$el.html(this.template({links: this.links}));
    return this;
  }
});
